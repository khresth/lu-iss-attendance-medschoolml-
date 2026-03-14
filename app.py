"""
MBChB Attendance Analysis Dashboard
Lancaster University Medical School

Single-file Gradio application for analysing student attendance and
placement records exported from LUSI/ITPI.

Run with:  python app.py
"""

import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import os
import logging

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PLACEMENT_PATTERNS  = r"(?i)(med\.plac|med\.othr|palliative care)"
SELF_STUDY_PATTERNS = r"(?i)med\.study|self-study|self study|self-study day"

# registerType value that indicates a self-certified absence
SELF_CERT_REGISTER_TYPE = "50"

# Cap on placement check-ins counted per student per day (clinical years)
CLINICAL_DAILY_CAP = 2

# Academic year base – Lancaster typically starts week of 25 August
ACADEMIC_YEAR_BASE_MONTH = 8
ACADEMIC_YEAR_BASE_DAY   = 25

# Boolean normalisation map used for present / selfCertInfo columns
BOOL_MAP = {"true": True, "false": False, True: True, False: False}

# ---------------------------------------------------------------------------
# Global state
# NOTE: single-user deployment only. Do not expose on a shared network without
# adding authentication (demo.launch(auth=...)) and migrating state to
# gr.State() for session isolation.
# ---------------------------------------------------------------------------
loaded_module_dfs:   dict  = {}
loaded_rotation_maps: dict = {"Y5R1": None, "Y3R1": None, "Y2": None, "Y4R1": None}
loaded_notes_df: pd.DataFrame = pd.DataFrame(
    columns=["studentId", "studentEmail", "notes"]
)

# ---------------------------------------------------------------------------
# Helper: academic week utilities
# ---------------------------------------------------------------------------

def get_academic_week(date: datetime) -> int:
    """Return the Lancaster academic week number for a given date.

    Week 1 begins on ACADEMIC_YEAR_BASE_DAY of ACADEMIC_YEAR_BASE_MONTH.
    Dates before that in the same calendar year belong to the prior academic year.
    """
    year = date.year if date.month >= ACADEMIC_YEAR_BASE_MONTH else date.year - 1
    base = datetime(year, ACADEMIC_YEAR_BASE_MONTH, ACADEMIC_YEAR_BASE_DAY)
    delta = (date - base).days
    return max(1, delta // 7 + 1)


def get_week_date_range(week: int, academic_year: int) -> str:
    """Return a human-readable date range string for an academic week."""
    base = datetime(academic_year, ACADEMIC_YEAR_BASE_MONTH, ACADEMIC_YEAR_BASE_DAY)
    week_start = base + timedelta(days=(week - 1) * 7)
    week_end   = week_start + timedelta(days=6)
    return f"{week_start.strftime('%d/%m/%Y')}-{week_end.strftime('%d/%m/%Y')}"


def _academic_year_for(dt: datetime) -> int:
    """Return the academic year integer (e.g. 2024 for 2024/25) for a datetime."""
    return dt.year if dt.month >= ACADEMIC_YEAR_BASE_MONTH else dt.year - 1


# ---------------------------------------------------------------------------
# Helper: rotation info lookup
# ---------------------------------------------------------------------------

def _rotation_info(sid: str, rotation_map: dict, year_label: str) -> tuple[str, str]:
    """Return (group_label, pattern_label) for a student from a rotation map."""
    info = rotation_map.get(str(sid), {})
    if year_label == "2":
        return info.get("hospital", "Unknown"), info.get("pattern", "N/A")
    if year_label == "5":
        return info.get("rotation", "Unknown"), info.get("pattern", "N/A")
    if year_label in ("3", "4"):
        g = info.get("group")
        return (f"Group {g}" if g is not None else "Unknown"), info.get("pattern", "N/A")
    return "N/A", "N/A"


# ---------------------------------------------------------------------------
# Data loading: rotation files
# ---------------------------------------------------------------------------

def _load_rotation_generic(
    file_paths: list,
    year_key: str,
    year_label: str,
    id_col_options: list[str],
    group_col: str,
    group_default: int,
) -> str:
    """Shared loader for Y2/Y3/Y4/Y5 rotation CSV files.

    Reads student ID, group, and pattern from each file and stores results
    in loaded_rotation_maps[year_key].
    """
    global loaded_rotation_maps
    if not file_paths:
        return f"No Year {year_label} rotation files uploaded."
    try:
        rotation_map: dict = {}
        loaded_count = 0
        for file_path in file_paths:
            if not file_path or not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, encoding="utf-8-sig")
            df.columns = df.columns.str.strip()

            # Resolve ID column
            id_col = next((c for c in id_col_options if c in df.columns), None)
            if id_col is None:
                logger.warning("Year %s rotation file missing ID column: %s", year_label, file_path)
                continue
            df[id_col] = df[id_col].astype(str).str.strip()

            for _, row in df.iterrows():
                sid = str(row[id_col])
                if year_label == "2":
                    trust = str(row.get("Trust (B1)", "Unknown")).strip().upper()
                    pattern = str(row.get("pattern", "N/A")).strip()
                    rotation_map[sid] = {"hospital": trust, "pattern": pattern}
                else:
                    try:
                        group = int(row.get(group_col, group_default))
                    except (ValueError, TypeError):
                        group = group_default
                    # Y5 uses Rotation 1 as the descriptive label; Y3/Y4 use Pattern
                    if year_label == "5":
                        rotation_val = str(row.get("Rotation 1", "Unknown"))
                        pattern_val  = str(row.get("Pattern", row.get("Rotation 1", "N/A")))
                    else:
                        rotation_val = str(row.get("Pattern", "N/A"))
                        pattern_val  = str(row.get("Pattern", "N/A"))
                    rotation_map[sid] = {
                        "group":    group,
                        "pattern":  pattern_val,
                        "rotation": rotation_val,
                    }
                loaded_count += 1

        loaded_rotation_maps[year_key] = rotation_map
        return f"Year {year_label}: {loaded_count} student(s) loaded from rotation file(s)."
    except Exception as exc:
        logger.exception("Failed loading Year %s rotation data", year_label)
        return f"Error loading Year {year_label} rotation files. Check the log for details."


def load_y5_rotation_data(file_paths: list) -> str:
    return _load_rotation_generic(file_paths, "Y5R1", "5", ["Student ID"], "Group", 1)


def load_y3_rotation_data(file_paths: list) -> str:
    return _load_rotation_generic(file_paths, "Y3R1", "3", ["Student ID"], "Group", 2)


def load_y4_rotation_data(file_paths: list) -> str:
    return _load_rotation_generic(file_paths, "Y4R1", "4", ["student_id", "Student ID"], "Group", 1)


def load_y2_rotation_data(file_paths: list) -> str:
    return _load_rotation_generic(file_paths, "Y2", "2", ["Student No."], "Group", 1)


# ---------------------------------------------------------------------------
# Data loading: notes (Book1.xlsx)
# ---------------------------------------------------------------------------

def load_notes(file_path: str | None) -> str:
    """Load student notes and emails from Book1.xlsx into loaded_notes_df."""
    global loaded_notes_df
    if not file_path or not os.path.exists(file_path):
        loaded_notes_df = pd.DataFrame(columns=["studentId", "studentEmail", "notes"])
        return "Book1.xlsx not uploaded. Notes and emails will be blank."
    try:
        df = pd.read_excel(file_path, sheet_name="Sheet1")
        df["Student ID"] = df["Student ID"].astype(str).str.strip()
        notes1 = df.get("Notes 1", pd.Series([""] * len(df))).fillna("")
        notes2 = df.get("Notes 2", pd.Series([""] * len(df))).fillna("")
        df["notes"] = (notes1 + notes2.apply(lambda x: f", {x}" if x.strip() else "")).str.strip(", ")
        loaded_notes_df = (
            df[["Student ID", "Email", "notes"]]
            .rename(columns={"Student ID": "studentId", "Email": "studentEmail"})
        )
        return f"Book1.xlsx loaded. {len(loaded_notes_df)} student record(s) with notes."
    except Exception as exc:
        logger.exception("Failed loading Book1.xlsx")
        loaded_notes_df = pd.DataFrame(columns=["studentId", "studentEmail", "notes"])
        return "Error loading Book1.xlsx. Notes will be blank. Check the file and try again."


# ---------------------------------------------------------------------------
# Data loading: LUSI attendance CSV
# ---------------------------------------------------------------------------

def load_and_clean_data(module: str, file_path: str) -> tuple:
    """Load and clean a LUSI attendance CSV file.

    Returns:
        (DataFrame | None, list[str] of dates, status message)
    """
    if not file_path or not os.path.exists(file_path):
        return None, [], f"File for {module} not provided."
    try:
        df = pd.read_csv(file_path, on_bad_lines="skip", encoding="utf-8-sig")

        # --- required columns ---
        missing = [c for c in ("studentId", "startDateTime") if c not in df.columns]
        if missing:
            return None, [], f"Missing required column(s): {', '.join(missing)}"

        df["studentId"] = df["studentId"].astype(str).str.strip()

        # --- parse dates ---
        df["startDateTime"] = pd.to_datetime(df["startDateTime"], errors="coerce").dt.tz_localize(None)
        df = df.dropna(subset=["startDateTime"])

        # --- boolean columns ---
        df["present"] = (
            df["present"].map(BOOL_MAP, na_action="ignore").fillna(False)
            if "present" in df.columns else False
        )
        df["selfCertInfo"] = (
            df["selfCertInfo"].map(BOOL_MAP, na_action="ignore").fillna(False)
            if "selfCertInfo" in df.columns else False
        )

        # --- cancelled column: normalise same as boolean cols ---
        if "cancelled" in df.columns:
            df["cancelled"] = df["cancelled"].map(BOOL_MAP, na_action="ignore").fillna(False)
        else:
            df["cancelled"] = False

        # --- self-cert register type overrides present ---
        if "registerType" in df.columns:
            df["registerType"] = df["registerType"].astype(str).str.strip()
            df.loc[df["registerType"] == SELF_CERT_REGISTER_TYPE, "present"] = False

        # --- drop cancelled rows ---
        df = df[~df["cancelled"]]

        # --- require core columns ---
        required = ["studentId", "firstName", "surname", "academicAdvisor", "startDateTime"]
        missing_core = [c for c in required if c not in df.columns]
        if missing_core:
            return None, [], f"Missing required column(s): {', '.join(missing_core)}"
        df = df.dropna(subset=required)
        if df.empty:
            return None, [], "No valid data rows after cleaning."

        # --- deduplicate placement check-ins within 10 minutes ---
        placement_mask = df["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False)
        dedup_msg = ""
        if placement_mask.any():
            plac = df[placement_mask].copy().sort_values(["studentId", "startDateTime"])
            plac["time_diff"] = plac.groupby("studentId")["startDateTime"].diff()
            plac = plac[(plac["time_diff"].isna()) | (plac["time_diff"] >= timedelta(minutes=10))]
            plac = plac.drop(columns=["time_diff"])
            removed = placement_mask.sum() - len(plac)
            if removed > 0:
                dedup_msg = f" ({removed} duplicate placement check-ins within 10 min removed)"
            df = pd.concat([df[~placement_mask], plac]).sort_values(
                ["studentId", "startDateTime"]
            ).reset_index(drop=True)

        study_count = df["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False).sum()
        unique_dates = sorted(df["startDateTime"].dt.date.astype(str).unique())
        return (
            df,
            unique_dates,
            f"{module}: {len(df)} row(s) loaded, {study_count} MED.STUDY event(s) excluded from metrics{dedup_msg}",
        )
    except Exception as exc:
        logger.exception("Failed loading module %s", module)
        return None, [], f"Error loading {module}. Check the file format and try again."


# ---------------------------------------------------------------------------
# Load all files (orchestrator called by the Load button)
# ---------------------------------------------------------------------------

def load_all_files(book1_file, y5_files, y3_files, y4_files, y2_files, module_files):
    global loaded_module_dfs
    loaded_module_dfs.clear()
    messages: list[str] = []

    messages.append(load_notes(book1_file))
    messages.append(load_y5_rotation_data(y5_files or []))
    messages.append(load_y3_rotation_data(y3_files or []))
    messages.append(load_y4_rotation_data(y4_files or []))
    messages.append(load_y2_rotation_data(y2_files or []))

    available_modules: list[str] = []
    for fpath in (module_files or []):
        if not fpath or not os.path.exists(fpath):
            continue
        fname = os.path.basename(fpath).lower()
        if fname.startswith("lusi_mbchb") and fname.endswith(".csv"):
            module_code = fname.replace("lusi_mbchb", "").replace(".csv", "").upper()
            df, dates, msg = load_and_clean_data(module_code, fpath)
            messages.append(msg)
            if df is not None:
                loaded_module_dfs[module_code] = (df, dates)
                available_modules.append(module_code)

    # Rotation-only pseudo-modules
    for key in ("Y5R1", "Y3R1", "Y4R1"):
        if loaded_rotation_maps.get(key):
            available_modules.append(key)

    if not available_modules:
        available_modules = ["No modules loaded"]

    return (
        "\n".join(messages),
        gr.update(choices=available_modules, value=available_modules[0] if available_modules else None),
        "Files loaded. Select a module and click Analyse.",
    )


# ---------------------------------------------------------------------------
# Student search
# ---------------------------------------------------------------------------

def find_student(first_name: str) -> str:
    if not first_name or not first_name.strip():
        return "Enter a first name to search."
    term = first_name.strip().lower()
    found = []
    for mod, (df, _) in loaded_module_dfs.items():
        for col in ("firstName", "Forename", "First name"):
            if col in df.columns and df[col].astype(str).str.lower().str.contains(term, na=False).any():
                found.append(mod)
                break
    return f"Found in module(s): {', '.join(found)}" if found else "No matches found."


# ---------------------------------------------------------------------------
# Date dropdown updater
# ---------------------------------------------------------------------------

def update_date_dropdowns(module: str):
    if module in ("Y5R1", "Y3R1", "Y4R1"):
        return (
            gr.update(choices=["N/A"], value="N/A"),
            gr.update(choices=["N/A"], value="N/A"),
            "Rotation-only module selected. No date range needed.",
        )
    if module not in loaded_module_dfs:
        return gr.update(choices=["No data"]), gr.update(choices=["No data"]), "Module not loaded."

    df, _ = loaded_module_dfs[module]
    if df.empty:
        return gr.update(choices=["No dates"]), gr.update(choices=["No dates"]), "No dates available."

    date_strings = (
        pd.date_range(start=df["startDateTime"].min().date(), end=df["startDateTime"].max().date(), freq="D")
        .strftime("%Y-%m-%d")
        .tolist()
    )
    return (
        gr.update(choices=date_strings, value=date_strings[0]),
        gr.update(choices=date_strings, value=date_strings[-1]),
        f"Date range for {module}: {date_strings[0]} to {date_strings[-1]}",
    )


# ---------------------------------------------------------------------------
# Per-student attendance graph
# ---------------------------------------------------------------------------

def plot_student_attendance(module: str, student_selection: str):
    if module in ("Y5R1", "Y3R1", "Y4R1"):
        return go.Figure(), "Graph not available for rotation-only modules."
    if not student_selection:
        return go.Figure(), "Select a student from the list."
    match = re.search(r"\((\d+)\)", student_selection)
    if not match:
        return go.Figure(), "Could not parse student ID from selection."
    student_id = match.group(1)
    if module not in loaded_module_dfs:
        return go.Figure(), "Module data not loaded."

    df, _ = loaded_module_dfs[module]
    sdf = df[df["studentId"] == student_id].sort_values("startDateTime").copy()
    if sdf.empty:
        return go.Figure(), f"No records found for student {student_id}."

    sdf["cum_present"] = sdf["present"].astype(int).cumsum()
    sdf["cum_events"]  = range(1, len(sdf) + 1)
    sdf["cum_rate"]    = sdf["cum_present"] / sdf["cum_events"] * 100
    overall = df["present"].mean() * 100

    name = f"{sdf['firstName'].iloc[0]} {sdf['surname'].iloc[0]}"
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sdf["startDateTime"], y=sdf["cum_rate"],
        mode="lines+markers",
        name=f"{name}",
        line=dict(color="#22a352", width=2.5),
        marker=dict(size=5, color="#22a352"),
    ))
    fig.add_trace(go.Scatter(
        x=[sdf["startDateTime"].min(), sdf["startDateTime"].max()],
        y=[overall, overall],
        mode="lines",
        name=f"Module average ({overall:.1f}%)",
        line=dict(color="#FF0000", dash="dash", width=2),
    ))
    fig.update_layout(
        title=f"Cumulative attendance - {name} (MBChB {module})",
        xaxis_title="Date",
        yaxis_title="Cumulative Attendance (%)",
        yaxis=dict(range=[0, 100]),
        xaxis=dict(tickangle=45),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=60, b=60, l=60, r=20),
    )

    absences = sdf[~sdf["present"]][["eventDescription", "startDateTime"]]
    if absences.empty:
        absence_text = "No absences recorded in this module."
    else:
        lines = [f"  {r.startDateTime.strftime('%Y-%m-%d %H:%M')}  |  {r.eventDescription}"
                 for _, r in absences.iterrows()]
        absence_text = f"Absent events ({len(absences)}):\n" + "\n".join(lines)
    return fig, absence_text


# ---------------------------------------------------------------------------
# Attendance analysis helpers
# ---------------------------------------------------------------------------

def _build_non_placement_table(
    filtered: pd.DataFrame,
    all_students: pd.DataFrame,
    thresh_val: float,
    show_self_cert: bool,
    sort_order: str,
    secondary_sort_by_surname: bool,
) -> tuple[str, list[str]]:
    """Compute non-placement attendance and return (html, student_choices)."""
    non_med = filtered[
        ~filtered["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False) &
        ~filtered["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False)
    ]

    if not non_med.empty:
        att_pct = (
            non_med.groupby("studentId")["present"]
            .mean()
            .mul(100)
            .reset_index(name="attendance_percentage")
        )
        att_pct["studentId"] = att_pct["studentId"].astype(str)
    else:
        att_pct = pd.DataFrame(columns=["studentId", "attendance_percentage"])

    # Students with no events in range: shown as 100% (they had nothing scheduled)
    att = all_students.merge(att_pct[["studentId", "attendance_percentage"]], on="studentId", how="left")
    att["attendance_percentage"] = att["attendance_percentage"].fillna(100.0)

    below = att[att["attendance_percentage"] <= thresh_val].copy()

    if show_self_cert:
        selfcert_ids = filtered[filtered["selfCertInfo"]]["studentId"].unique()
        below = below[below["studentId"].isin(selfcert_ids)]

    below = below.merge(loaded_notes_df, on="studentId", how="left").fillna({"notes": "", "studentEmail": ""})

    # Surname sort OVERRIDES all other sorting when ticked
    if secondary_sort_by_surname:
        below = below.sort_values(["surname", "firstName"]).reset_index(drop=True)
    else:
        ascending = sort_order == "Lowest to Highest"
        below = below.sort_values("attendance_percentage", ascending=ascending).reset_index(drop=True)

    if below.empty:
        html = _info_box("No students found at or below this threshold.")
    else:
        display = below.rename(columns={
            "studentId":            "Student ID",
            "firstName":            "First Name",
            "surname":              "Surname",
            "studentEmail":         "Student Email",
            "attendance_percentage": "Attendance (%)",
        }).drop(columns=["academicAdvisor", "notes"], errors="ignore").round(2)
        html = (
            f"<p><strong>{len(below)} student(s) found at or below {thresh_val:.4g}%.</strong></p>"
            + _styled_table(display)
        )

    choices = [f"{r['firstName']} {r['surname']} ({r['studentId']})" for _, r in below.iterrows()]
    return html, choices


def _build_placement_table(
    filtered: pd.DataFrame,
    all_students: pd.DataFrame,
    start_dt: datetime,
    year_label: str,
    rotation_map: dict,
    placement_sort: str,
    secondary_sort_by_surname: bool = False,
) -> str:
    """Compute placement attendance table and return HTML."""
    med = filtered[
        filtered["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False) &
        ~filtered["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False) &
        filtered["present"]
    ].copy()

    if med.empty:
        placement_df = all_students.copy()
        placement_df[["Group", "Pattern"]] = placement_df["studentId"].apply(
            lambda sid: pd.Series(_rotation_info(sid, rotation_map, year_label))
        )
        placement_df["Total_Days_Attended"] = 0
        placement_df["Med.Plac Dates"]      = "None found"
        placement_df["Week_Range"]          = "None"
    else:
        med["week"] = med["startDateTime"].apply(get_academic_week)
        med["date"] = med["startDateTime"].dt.date
        acad_year   = _academic_year_for(start_dt)

        rows = []
        for sid in med["studentId"].unique():
            group_lbl, pat_lbl = _rotation_info(sid, rotation_map, year_label)
            s = med[med["studentId"] == sid].copy()
            weekly = (
                s.groupby(["studentId", "firstName", "surname", "week"])["date"]
                .nunique()
                .reset_index(name="Days_Attended")
            )
            weekly["Period_Label"] = weekly["week"].apply(lambda w: get_week_date_range(w, acad_year))
            weekly["Group"]   = group_lbl
            weekly["Pattern"] = pat_lbl
            rows.append(weekly)

        weekly_days = pd.concat(rows, ignore_index=True)
        all_placement = (
            weekly_days.groupby(["studentId", "firstName", "surname", "Group", "Pattern"])
            .agg(
                Total_Days_Attended=("Days_Attended", "sum"),
                Week_Range=("Period_Label", lambda x: ", ".join(sorted(set(x)))),
            )
            .reset_index()
        )
        dates_agg = (
            med.groupby("studentId", as_index=False)["startDateTime"]
            .agg(lambda x: ", ".join(sorted(set(x.dt.strftime("%Y-%m-%d")))))
            .rename(columns={"startDateTime": "Med.Plac Dates"})
        )
        all_placement = all_placement.merge(dates_agg, on="studentId", how="left")
        all_placement["Med.Plac Dates"] = all_placement["Med.Plac Dates"].fillna("None found")

        placement_df = all_students.merge(
            all_placement, on=["studentId", "firstName", "surname"], how="left"
        ).fillna({
            "Total_Days_Attended": 0,
            "Med.Plac Dates": "None found",
            "Week_Range": "None",
            "Group":   "N/A",
            "Pattern": "N/A",
        })

    placement_df = placement_df.merge(loaded_notes_df, on="studentId", how="left").fillna({"studentEmail": ""})
    placement_df = placement_df.rename(columns={
        "studentId":    "Student ID",
        "firstName":    "First Name",
        "surname":      "Surname",
        "studentEmail": "Student Email",
    })[["Student ID", "First Name", "Surname", "Group", "Pattern",
        "Student Email", "Med.Plac Dates", "Week_Range", "Total_Days_Attended"]]

    ascending_p = placement_sort == "Least Placement Days First"
    if secondary_sort_by_surname:
        placement_df = placement_df.sort_values(["Surname", "First Name"]).reset_index(drop=True)
    else:
        placement_df = placement_df.sort_values("Total_Days_Attended", ascending=ascending_p).reset_index(drop=True)

    header = (
        f"<h3>Year {year_label} Medical Placement Attendance</h3>"
        "<p>Counts distinct days with at least one <em>present</em> placement check-in "
        "(MED.PLAC, MED.OTHR, palliative care). MED.STUDY excluded. All students shown.</p>"
    )
    return header + _styled_table(placement_df)


def _build_placement_absences_table(
    filtered: pd.DataFrame,
    is_clinical: bool,
    rotation_map: dict | None,
    year_label: str | None,
) -> str:
    """Return HTML table of placement events where present=False."""
    med_abs = filtered[
        filtered["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False) &
        ~filtered["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False) &
        ~filtered["present"]
    ].copy()

    if med_abs.empty:
        return _info_box("No placement absences (present=False) found in this date range.")

    medplac_df = med_abs[["studentId", "firstName", "surname", "eventDescription", "startDateTime"]].copy()
    medplac_df["Date"] = medplac_df["startDateTime"].dt.strftime("%Y-%m-%d %H:%M")

    if is_clinical and rotation_map:
        medplac_df["Group"] = medplac_df["studentId"].astype(str).map(
            lambda sid: _rotation_info(sid, rotation_map, year_label)[0]
        )
        cols = ["Student ID", "First Name", "Surname", "Group", "Student Email", "Event Description", "Date", "Notes"]
    else:
        medplac_df["Group"] = "N/A"
        cols = ["Student ID", "First Name", "Surname", "Student Email", "Event Description", "Date", "Notes"]

    medplac_df = medplac_df.merge(loaded_notes_df, on="studentId", how="left").fillna({"notes": "", "studentEmail": ""})
    medplac_df = medplac_df.rename(columns={
        "studentId":       "Student ID",
        "firstName":       "First Name",
        "surname":         "Surname",
        "studentEmail":    "Student Email",
        "eventDescription":"Event Description",
        "notes":           "Notes",
    })

    return (
        "<h3>Placement Absences (present=False)</h3>"
        + _styled_table(medplac_df[cols])
    )


# ---------------------------------------------------------------------------
# Main analysis entry point
# ---------------------------------------------------------------------------

def analyze_attendance(
    module, start_date, end_date, threshold,
    show_self_cert, sort_order, secondary_sort_by_surname, placement_sort,
):
    no_data = (
        "Please select a module and valid date range.",
        _info_box("Select a module and date range, then click Analyse."),
        "",
        gr.update(choices=[], value=None),
        None,
        _info_box("No placement data yet."),
        _info_box("No placement absence data yet."),
    )

    if start_date is None or str(start_date) in ("N/A", "No dates", "No data"):
        return no_data

    # --- Rotation-only view ---
    if module in ("Y5R1", "Y3R1", "Y4R1"):
        rot_key = module
        if not loaded_rotation_maps.get(rot_key):
            return ("Rotation data not loaded.",) + no_data[1:]
        df = pd.DataFrame.from_dict(loaded_rotation_maps[rot_key], orient="index").reset_index()
        df = df.rename(columns={"index": "Student ID"})
        df = df.merge(loaded_notes_df, left_on="Student ID", right_on="studentId", how="left").fillna(
            {"studentEmail": "", "notes": ""}
        )
        label_col = "rotation" if "rotation" in df.columns else "Pattern"
        student_table_html = df[["Student ID", "studentEmail", "group", label_col, "notes"]].rename(
            columns={"studentEmail": "Email", "notes": "Notes"}
        ).to_html(index=False)
        group_summary = df.groupby("group").size().reset_index(name="Students").to_html(index=False)
        html = f"<h3>Rotation Summary</h3>{group_summary}<br><h3>Students</h3>{student_table_html}"
        return "Rotation data displayed.", html, "", gr.update(choices=[], value=None), None, _info_box("N/A for rotation view."), _info_box("N/A for rotation view.")

    if module not in loaded_module_dfs:
        return ("Module not loaded.",) + no_data[1:]

    df, _ = loaded_module_dfs[module]

    # --- parse dates ---
    try:
        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)
    except (ValueError, TypeError):
        return ("Invalid date format. Please use the date dropdowns.",) + no_data[1:]

    # --- parse threshold ---
    try:
        thresh_val = float(threshold)
    except (ValueError, TypeError):
        thresh_val = 50.0

    filtered = df[df["startDateTime"].between(start_dt, end_dt)]
    if filtered.empty:
        return (
            "No events found in the selected date range.",
            _info_box("No events found in the selected date range."),
            "", gr.update(choices=[], value=None), None,
            _info_box("No events in range."),
            _info_box("No events in range."),
        )

    # Students from the FULL dataset (not just the filtered range) so names are always available
    all_students = (
        df[["studentId", "firstName", "surname", "academicAdvisor"]]
        .drop_duplicates("studentId")
        .copy()
    )
    all_students["studentId"] = all_students["studentId"].astype(str)

    # --- non-placement attendance ---
    att_html, student_choices = _build_non_placement_table(
        filtered, all_students, thresh_val,
        show_self_cert, sort_order, secondary_sort_by_surname,
    )

    # --- placement analysis ---
    is_clinical = module[:1].isdigit() and module[0] in ("2", "3", "4", "5")
    year_label  = module[0] if is_clinical else None
    rotation_map_key = {"2": "Y2", "3": "Y3R1", "4": "Y4R1", "5": "Y5R1"}.get(year_label, "")
    rotation_map = loaded_rotation_maps.get(rotation_map_key, {}) or {}

    if is_clinical:
        placement_html = _build_placement_table(
            filtered, all_students, start_dt, year_label, rotation_map, placement_sort,
            secondary_sort_by_surname=secondary_sort_by_surname,
        )
    else:
        placement_html = _info_box("Placement analysis applies to clinical years (Y2-Y5) only.")

    abs_html = _build_placement_absences_table(filtered, is_clinical, rotation_map, year_label)

    return (
        f"Analysis complete. {len(student_choices)} student(s) at or below threshold.",
        att_html,
        "",
        gr.update(choices=student_choices, value=None),
        None,
        placement_html,
        abs_html,
    )


# ---------------------------------------------------------------------------
# Macro attendance view
# ---------------------------------------------------------------------------

def macro_attendance(module: str, days_back: int) -> str:
    if module not in loaded_module_dfs:
        return _info_box("Module not loaded.")

    df, _ = loaded_module_dfs[module]
    cutoff = datetime.now() - timedelta(days=days_back)
    all_students = df[["studentId", "firstName", "surname"]].drop_duplicates("studentId").copy()
    all_students["studentId"] = all_students["studentId"].astype(str)

    med_events = df[
        df["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False) &
        ~df["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False) &
        (df["startDateTime"] >= cutoff)
    ].copy()

    if med_events.empty:
        counts = all_students.copy()
        counts["Placement_Count"] = 0
    else:
        med_events["date"]      = med_events["startDateTime"].dt.date
        med_events["studentId"] = med_events["studentId"].astype(str)
        is_clinical_mac = module[:1].isdigit() and module[0] in ("2", "3", "4", "5")
        max_per_day = CLINICAL_DAILY_CAP if is_clinical_mac else 999
        capped = (
            med_events.groupby(["studentId", "date"])
            .size()
            .reset_index(name="daily_count")
        )
        capped["capped_count"] = capped["daily_count"].clip(upper=max_per_day)
        count_from = capped.groupby("studentId")["capped_count"].sum().reset_index(name="Placement_Count")
        counts = all_students.merge(count_from, on="studentId", how="left")
        counts["Placement_Count"] = counts["Placement_Count"].fillna(0)

    rot_key = {"2": "Y2", "3": "Y3R1", "4": "Y4R1", "5": "Y5R1"}.get(
        module[0] if module[:1].isdigit() else "", ""
    )
    rotation_map = loaded_rotation_maps.get(rot_key, {}) or {}
    year_label_mac = module[0] if module[:1].isdigit() and module[0] in ("2","3","4","5") else None

    if year_label_mac:
        counts[["Group", "Pattern"]] = counts["studentId"].apply(
            lambda sid: pd.Series(_rotation_info(sid, rotation_map, year_label_mac))
        )
    else:
        counts["Group"] = counts["Pattern"] = "N/A"

    counts = (
        counts.merge(loaded_notes_df, on="studentId", how="left")
        .fillna({"studentEmail": ""})
        .sort_values("Placement_Count")
    )
    max_per_day_label = CLINICAL_DAILY_CAP if (year_label_mac is not None) else 999
    col_label = f"Placement Days (last {days_back} days)"
    display = counts.rename(columns={
        "studentId":       "Student ID",
        "firstName":       "First Name",
        "surname":         "Surname",
        "studentEmail":    "Student Email",
        "Group":           "Group/Rotation",
        "Placement_Count": col_label,
    })[["Student ID", "First Name", "Surname", "Student Email", "Group/Rotation", "Pattern", col_label]]

    header = (
        f"<h3>Placement Macro View – Last {days_back} Days</h3>"
        f"<p>Includes MED.PLAC and MED.OTHR. Daily cap: {max_per_day_label}. MED.STUDY excluded. All students shown.</p>"
    )
    return header + _styled_table(display)


# ---------------------------------------------------------------------------
# Self-certified events view
# ---------------------------------------------------------------------------

def self_certified_events(module: str, start_date, end_date) -> str:
    if module not in loaded_module_dfs:
        return _info_box("Module not loaded.")
    if start_date is None or str(start_date) in ("N/A", "No dates"):
        return _info_box("Please select a valid date range first.")

    df, _ = loaded_module_dfs[module]

    try:
        start_dt = pd.to_datetime(start_date)
        end_dt   = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)
    except (ValueError, TypeError):
        return _info_box("Invalid date format. Use the date dropdowns.")

    filtered = df[df["startDateTime"].between(start_dt, end_dt)].copy()
    if filtered.empty:
        return _info_box("No events in the selected date range.")
    if "registerType" not in filtered.columns:
        return _info_box("No registerType column found in this data.")

    selfcert_df = filtered[filtered["registerType"] == SELF_CERT_REGISTER_TYPE].copy()
    if selfcert_df.empty:
        return _info_box("No self-certified events (registerType=50) in this date range.")

    selfcert_df = selfcert_df[~selfcert_df["eventDescription"].str.contains(SELF_STUDY_PATTERNS, na=False)]
    if selfcert_df.empty:
        return _info_box("No qualifying self-certified events after excluding self-study events.")

    selfcert_df["date"]      = selfcert_df["startDateTime"].dt.date
    selfcert_df["studentId"] = selfcert_df["studentId"].astype(str)

    is_placement = selfcert_df["eventDescription"].str.contains(PLACEMENT_PATTERNS, na=False)
    plac_self    = selfcert_df[is_placement].copy()
    non_plac     = selfcert_df[~is_placement].copy()

    counted_events: list = []
    if not plac_self.empty:
        daily = plac_self.groupby(["studentId", "date"]).size().reset_index(name="daily_count")
        daily["counted"] = daily["daily_count"].clip(upper=CLINICAL_DAILY_CAP)
        for _, row in daily[daily["counted"] > 0].iterrows():
            counted_events.extend([(row["studentId"], row["date"])] * int(row["counted"]))
    if not non_plac.empty:
        counted_events += list(zip(non_plac["studentId"], non_plac["date"]))

    if not counted_events:
        return _info_box("No counted self-certified events after applying rules.")

    counted_df = pd.DataFrame(counted_events, columns=["studentId", "date"])
    summary = (
        counted_df.groupby("studentId")
        .agg(Count=("date", "size"), Dates=("date", lambda x: ", ".join(sorted(x.astype(str)))))
        .reset_index()
    )
    names   = filtered[["studentId", "firstName", "surname"]].drop_duplicates("studentId")
    summary = (
        summary.merge(names, on="studentId", how="left")
        .merge(loaded_notes_df[["studentId", "studentEmail"]], on="studentId", how="left")
        .fillna({"firstName": "", "surname": "", "studentEmail": ""})
        .sort_values(["Count", "surname"], ascending=[False, True])
    )
    final = summary[["studentId", "firstName", "surname", "studentEmail", "Dates", "Count"]].rename(columns={
        "studentId":    "Student ID",
        "firstName":    "First Name",
        "surname":      "Surname",
        "studentEmail": "Student Email",
        "Dates":        "Self-Cert Dates",
        "Count":        "Total Count",
    })

    header = (
        "<h3>Self-Certified Events</h3>"
        "<p>Includes all registerType=50 events. Placement events capped at 2 per student per day. "
        "Self-study events excluded.</p>"
    )
    return header + f"<p><strong>{len(final)} student(s) with self-certified absences.</strong></p>" + _styled_table(final)


# ---------------------------------------------------------------------------
# HTML rendering helpers
# ---------------------------------------------------------------------------

_TABLE_CSS = """
<style>
  .dash-table { border-collapse: collapse; width: 100%; font-family: inherit; font-size: 13px; }
  .dash-table th { padding: 8px 12px; text-align: left; border-bottom: 2px solid #ccc; }
  .dash-table td { padding: 7px 12px; border-bottom: 1px solid #e5e5e5; }
  .info-box { padding: 10px 14px; border: 1px solid #e5e5e5; font-size: 13px;
              border-radius: 4px; margin: 8px 0; }
</style>
"""

def _styled_table(df: pd.DataFrame) -> str:
    """Render a DataFrame as a styled HTML table. HTML-escapes all cell content."""
    rows_html = ""
    for _, row in df.iterrows():
        cells = "".join(
            f"<td>{str(v).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')}</td>"
            for v in row
        )
        rows_html += f"<tr>{cells}</tr>"
    headers = "".join(f"<th>{h}</th>" for h in df.columns)
    return (
        _TABLE_CSS
        + f"<table class='dash-table'><thead><tr>{headers}</tr></thead><tbody>{rows_html}</tbody></table>"
    )


def _info_box(msg: str) -> str:
    return _TABLE_CSS + f"<div class='info-box'>{msg}</div>"


# ---------------------------------------------------------------------------
# Gradio UI
# ---------------------------------------------------------------------------

_HEADER_CSS = """
<style>
  .section-title { font-size: 15px; font-weight: 700;
                   border-bottom: 1px solid #e5e5e5; padding-bottom: 4px; margin-bottom: 8px; }
</style>
"""

def build_ui() -> gr.Blocks:
    with gr.Blocks(
        title="MBChB Attendance Dashboard",
        css="""
        button.primary, .gr-button.primary, button[variant="primary"] {
            background: #ea580c !important;
            border-color: #ea580c !important;
            color: #fff !important;
        }
        button.primary:hover, .gr-button.primary:hover, button[variant="primary"]:hover {
            background: #c2460a !important;
            border-color: #c2460a !important;
        }
        """,
    ) as demo:

        gr.HTML(_HEADER_CSS)

        gr.Markdown("## MBChB Attendance Dashboard")
        gr.Markdown("Lancaster University Medical School &nbsp;|&nbsp; Upload your files below, then click Load Data.")

        # ── File uploads ─────────────────────────────────────────────
        with gr.Group():
            gr.HTML("<div class='section-title'>Step 1 &mdash; Upload Files</div>")
            with gr.Row():
                book1_upload   = gr.File(label="Book1.xlsx (notes & emails)", file_types=[".xlsx"])
                module_uploads = gr.File(
                    label="Attendance logs (lusi_mbchb*.csv) — multiple files allowed",
                    file_types=[".csv"], file_count="multiple",
                )
            with gr.Row():
                y5_upload = gr.File(label="Year 5 rotations (y5r*.csv)", file_types=[".csv"], file_count="multiple")
                y4_upload = gr.File(label="Year 4 rotations (y4r*.csv)", file_types=[".csv"], file_count="multiple")
                y3_upload = gr.File(label="Year 3 rotations (y3r*.csv)", file_types=[".csv"], file_count="multiple")
                y2_upload = gr.File(label="Year 2 rotations (y2r*.csv)", file_types=[".csv"], file_count="multiple")

            load_btn    = gr.Button("Load Data", variant="primary", size="lg")
            load_status = gr.Textbox(label="Load status", lines=4, interactive=False)

        # ── Module + dates ───────────────────────────────────────────
        with gr.Group():
            gr.HTML("<div class='section-title'>Step 2 &mdash; Select Module and Date Range</div>")
            with gr.Row():
                module_dd    = gr.Dropdown(label="Module", choices=[], interactive=True, scale=2)
                start_date_dd = gr.Dropdown(label="Start date", scale=3)
                end_date_dd   = gr.Dropdown(label="End date",   scale=3)

        # ── Filters ──────────────────────────────────────────────────
        with gr.Group():
            gr.HTML("<div class='section-title'>Step 3 &mdash; Set Filters</div>")
            with gr.Row():
                thresh_number = gr.Number(
                    label="Attendance threshold (%) — show students at or below this",
                    value=50.0, minimum=0.0, maximum=100.0, step=0.1, precision=4, scale=2,
                )
                sort_dd       = gr.Dropdown(
                    choices=["Lowest to Highest", "Highest to Lowest"],
                    label="Sort attendance by", value="Lowest to Highest", scale=2,
                )
                plac_sort_dd  = gr.Dropdown(
                    choices=["Least Placement Days First", "Most Placement Days First"],
                    label="Sort placement by", value="Least Placement Days First", scale=2,
                )
            with gr.Row():
                sec_sort_cb   = gr.Checkbox(label="Sort alphabetically by surname (overrides all other sort options)", value=True)
                self_cert_cb  = gr.Checkbox(label="Show only students with self-certified absences", value=False)

        # ── Student search ───────────────────────────────────────────
        with gr.Group():
            gr.HTML("<div class='section-title'>Student Search</div>")
            with gr.Row():
                student_search = gr.Textbox(label="Find student by first name", scale=4)
                search_btn     = gr.Button("Search", scale=1)
            search_result = gr.Textbox(label="Result", lines=1, interactive=False)

        # ── Analyse button + status ──────────────────────────────────
        analyze_btn = gr.Button("Analyse Attendance", variant="primary", size="lg")
        status_out  = gr.Textbox(label="Status", lines=2, interactive=False)

        # ── Output tabs ──────────────────────────────────────────────
        with gr.Tabs():
            with gr.Tab("Attendance Summary"):
                gr.HTML("<p>Students at or below the attendance threshold for non-placement sessions.</p>")
                summary_table = gr.HTML()

            with gr.Tab("Student Detail"):
                gr.HTML("<p>Select a student from the Attendance Summary results to see their individual trend.</p>")
                student_radio   = gr.Radio(label="Select student", choices=[])
                attendance_graph = gr.Plot()
                absence_text    = gr.Textbox(label="Absence log", lines=10, interactive=False)

            with gr.Tab("Placement Analysis"):
                gr.HTML("<p>Days with at least one present placement check-in per student (present=True only).</p>")
                placement_table = gr.HTML()

            with gr.Tab("Placement Absences"):
                gr.HTML("<p>Placement events where present=False (missed or self-certified placement sessions).</p>")
                self_cert_placement_table = gr.HTML()

            with gr.Tab("Placement Macro"):
                gr.HTML("<p>Quick overview of placement activity over a rolling window, independent of the date range above.</p>")
                with gr.Row():
                    days_slider = gr.Slider(7, 365, value=30, step=1, label="Look back (days)", scale=4)
                    macro_btn   = gr.Button("Refresh", scale=1)
                macro_table = gr.HTML()

            with gr.Tab("Self-Certified Events"):
                gr.HTML("<p>All registerType=50 events in the selected date range, with a weighted daily count.</p>")
                self_cert_refresh = gr.Button("Refresh", variant="primary")
                self_cert_table   = gr.HTML()

        # ── Event wiring ─────────────────────────────────────────────
        load_btn.click(
            load_all_files,
            inputs=[book1_upload, y5_upload, y3_upload, y4_upload, y2_upload, module_uploads],
            outputs=[load_status, module_dd, status_out],
        )
        module_dd.change(
            update_date_dropdowns,
            inputs=module_dd,
            outputs=[start_date_dd, end_date_dd, status_out],
        )
        search_btn.click(find_student, inputs=student_search, outputs=search_result)
        analyze_btn.click(
            analyze_attendance,
            inputs=[module_dd, start_date_dd, end_date_dd, thresh_number,
                    self_cert_cb, sort_dd, sec_sort_cb, plac_sort_dd],
            outputs=[status_out, summary_table, absence_text,
                     student_radio, attendance_graph,
                     placement_table, self_cert_placement_table],
        )
        student_radio.change(
            plot_student_attendance,
            inputs=[module_dd, student_radio],
            outputs=[attendance_graph, absence_text],
        )
        macro_btn.click(macro_attendance, inputs=[module_dd, days_slider], outputs=macro_table)
        self_cert_refresh.click(
            self_certified_events,
            inputs=[module_dd, start_date_dd, end_date_dd],
            outputs=self_cert_table,
        )

    return demo


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    demo = build_ui()
    demo.launch()


if __name__ == "__main__":
    main()
