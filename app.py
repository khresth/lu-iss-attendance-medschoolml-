import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import os

# Global state
loaded_module_dfs = {}
loaded_rotation_maps = {"Y5R1": None, "Y3R1": None, "Y2": None, "Y4R1": None}
loaded_notes_df = pd.DataFrame(columns=['studentId', 'studentEmail', 'notes'])

GROUP_EXPECTED_DAYS_Y5 = {1: 4, 2: 3}
GROUP_EXPECTED_DAYS_Y3 = {1: 2, 2: 1}
GROUP_EXPECTED_DAYS_Y4 = {1: 3}

PLACEMENT_PATTERNS = r"(?i)(med\.plac|med\.othr|palliative care)"
SELF_STUDY_PATTERNS = r"(?i)med\.study|self-study|self study|self-study day"


def load_and_clean_data(module, file_path):
    if not file_path or not os.path.exists(file_path):
        return None, [], f"File for {module} not provided."
    try:
        if module in ["Y5R1", "Y3R1", "Y4R1"]:
            df = pd.read_csv(file_path)
            df_key = 'Student ID' if 'Student ID' in df.columns else 'student_id'
            df[df_key] = df[df_key].astype(str).str.strip()
            return df, [], f"Loaded rotation data: {len(df)} students"

        df = pd.read_csv(file_path, on_bad_lines="skip", encoding='utf-8-sig')
        if 'studentId' not in df.columns:
            return None, [], "Missing 'studentId' column."
        df['studentId'] = df['studentId'].astype(str).str.strip()
        if 'startDateTime' not in df.columns:
            return None, [], "Missing 'startDateTime' column."
        df['startDateTime'] = pd.to_datetime(df['startDateTime'], errors='coerce').dt.tz_localize(None)
        df = df.dropna(subset=['startDateTime'])
        if 'present' in df.columns:
            df['present'] = df['present'].map({'true': True, 'false': False, True: True, False: False}, na_action='ignore').fillna(False)
        else:
            df['present'] = False
        if 'selfCertInfo' in df.columns:
            df['selfCertInfo'] = df['selfCertInfo'].map({'true': True, 'false': False, True: True, False: False}, na_action='ignore').fillna(False)
        else:
            df['selfCertInfo'] = False
        df['cancelled'] = df.get('cancelled', pd.Series([False] * len(df), index=df.index))
        if 'registerType' in df.columns:
            df['registerType'] = df['registerType'].astype(str).str.strip()
            df.loc[df['registerType'] == '50', 'present'] = False
        df = df[df['cancelled'] == False]
        required = ['studentId', 'firstName', 'surname', 'academicAdvisor', 'startDateTime']
        if not all(col in df.columns for col in required):
            return None, [], "Missing required columns."
        df = df.dropna(subset=required)
        if df.empty:
            return None, [], "No valid data after cleaning."

        placement_mask = df['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)
        dedup_msg = ""
        if placement_mask.any():
            placement_df = df[placement_mask].copy()
            if not placement_df.empty:
                placement_df = placement_df.sort_values(['studentId', 'startDateTime'])
                placement_df['time_diff'] = placement_df.groupby('studentId')['startDateTime'].diff()
                placement_df['keep'] = (placement_df['time_diff'].isna()) | (placement_df['time_diff'] >= timedelta(minutes=10))
                deduped_placement = placement_df[placement_df['keep']].drop(columns=['time_diff', 'keep'])
                dedup_count = len(placement_df) - len(deduped_placement)
                dedup_msg = f" (deduplicated {dedup_count} placement check-ins within 10 min)" if dedup_count > 0 else ""
            df = pd.concat([df[~placement_mask], deduped_placement]).sort_values(['studentId', 'startDateTime']).reset_index(drop=True)

        self_study_count = len(df[df['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False)])
        unique_dates = sorted(df['startDateTime'].dt.date.astype(str).unique())
        return df, unique_dates, f"Loaded {len(df)} rows from {os.path.basename(file_path)} (excluded {self_study_count} MED.STUDY/self-study events){dedup_msg}"
    except Exception as e:
        return None, [], f"Error loading file: {str(e)}"


def load_y5_rotation_data(file_paths):
    global loaded_rotation_maps
    if not file_paths or len(file_paths) == 0:
        return "No Year 5 rotation files uploaded."
    try:
        rotation_map = {}
        loaded_count = 0
        for file_path in file_paths:
            if not file_path or not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            df['Student ID'] = df['Student ID'].astype(str).str.strip()
            for _, row in df.iterrows():
                sid = str(row['Student ID'])
                group = int(row.get('Group', 1))
                expected_days = GROUP_EXPECTED_DAYS_Y5.get(group, 3)
                rotation_map[sid] = {'group': group, 'expected_days': expected_days, 'rotation': row.get('Rotation 1', 'Unknown')}
                loaded_count += 1
        loaded_rotation_maps["Y5R1"] = rotation_map
        return f"{loaded_count} Year 5 rotation file(s) loaded successfully."
    except Exception as e:
        return f"Error loading Year 5 rotation files: {str(e)}"


def load_y3_rotation_data(file_paths):
    global loaded_rotation_maps
    if not file_paths or len(file_paths) == 0:
        return "No Year 3 rotation files uploaded."
    try:
        rotation_map = {}
        loaded_count = 0
        for file_path in file_paths:
            if not file_path or not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            df.columns = df.columns.str.strip()
            df['Student ID'] = df['Student ID'].astype(str).str.strip()
            for _, row in df.iterrows():
                sid = str(row['Student ID'])
                group = int(row.get('Group', 2))
                expected_days = GROUP_EXPECTED_DAYS_Y3.get(group, 1)
                rotation_map[sid] = {'group': group, 'expected_days': expected_days, 'rotation': row.get('Pattern', 'N/A')}
                loaded_count += 1
        loaded_rotation_maps["Y3R1"] = rotation_map
        return f"{loaded_count} Year 3 rotation file(s) loaded successfully."
    except Exception as e:
        return f"Error loading Year 3 rotation files: {str(e)}"


def load_y4_rotation_data(file_paths):
    global loaded_rotation_maps
    if not file_paths or len(file_paths) == 0:
        return "No Year 4 rotation files uploaded."
    try:
        rotation_map = {}
        loaded_count = 0
        for file_path in file_paths:
            if not file_path or not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            df.columns = df.columns.str.strip()
            df_key = 'student_id' if 'student_id' in df.columns else 'Student ID'
            df[df_key] = df[df_key].astype(str).str.strip()
            for _, row in df.iterrows():
                sid = str(row[df_key])
                group = int(row.get('Group', 1))
                expected_days = GROUP_EXPECTED_DAYS_Y4.get(group, 3)
                rotation_map[sid] = {'group': group, 'expected_days': expected_days, 'rotation': row.get('Pattern', 'N/A')}
                loaded_count += 1
        loaded_rotation_maps["Y4R1"] = rotation_map
        return f"{loaded_count} Year 4 rotation file(s) loaded successfully."
    except Exception as e:
        return f"Error loading Year 4 rotation files: {str(e)}"


def load_y2_rotation_data(file_paths):
    global loaded_rotation_maps
    if not file_paths or len(file_paths) == 0:
        return "No Year 2 rotation files uploaded."
    try:
        rotation_map = {}
        loaded_count = 0
        for file_path in file_paths:
            if not file_path or not os.path.exists(file_path):
                continue
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            df.columns = df.columns.str.strip()
            df['Student No.'] = df['Student No.'].astype(str).str.strip()
            for _, row in df.iterrows():
                sid = str(row['Student No.'])
                trust = row.get('Trust (B1)', 'Unknown').strip().upper()
                pattern = row.get('pattern', 'N/A').strip()
                rotation_map[sid] = {'hospital': trust, 'pattern': pattern}
                loaded_count += 1
        loaded_rotation_maps["Y2"] = rotation_map
        return f"{loaded_count} Year 2 rotation file(s) loaded successfully."
    except Exception as e:
        return f"Error loading Year 2 rotation files: {str(e)}"


def load_notes(file_path):
    global loaded_notes_df
    if not file_path or not os.path.exists(file_path):
        loaded_notes_df = pd.DataFrame(columns=['studentId', 'studentEmail', 'notes'])
        return "Book1.xlsx not uploaded – notes will be empty."
    try:
        df = pd.read_excel(file_path, sheet_name="Sheet1")
        df['Student ID'] = df['Student ID'].astype(str).str.strip()
        df['notes1'] = df.get('Notes 1', '').fillna('')
        df['notes2'] = df.get('Notes 2', '').fillna('')
        df['notes'] = df['notes1'] + (', ' + df['notes2'] if df['notes2'].str.strip().any() else '')
        df['notes'] = df['notes'].str.strip(', ')
        loaded_notes_df = df[['Student ID', 'Email', 'notes']].rename(columns={'Student ID': 'studentId', 'Email': 'studentEmail'})
        return "Book1.xlsx loaded successfully."
    except Exception as e:
        loaded_notes_df = pd.DataFrame(columns=['studentId', 'studentEmail', 'notes'])
        return f"Error loading Book1.xlsx: {str(e)}"


def load_all_files(book1_file, y5_files, y3_files, y4_files, y2_files, module_files):
    global loaded_module_dfs
    loaded_module_dfs.clear()
    messages = []
    messages.append(load_notes(book1_file))
    messages.append(load_y5_rotation_data(y5_files))
    messages.append(load_y3_rotation_data(y3_files))
    messages.append(load_y4_rotation_data(y4_files))
    messages.append(load_y2_rotation_data(y2_files))
    available_modules = []
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
    if loaded_rotation_maps.get("Y5R1"):
        available_modules.append("Y5R1")
    if loaded_rotation_maps.get("Y3R1"):
        available_modules.append("Y3R1")
    if loaded_rotation_maps.get("Y4R1"):
        available_modules.append("Y4R1")
    if not available_modules:
        available_modules = ["No modules loaded – upload at least one file"]
    return "\n".join(messages), gr.update(choices=available_modules), "Files loaded. Select a module to analyze."


def find_student(first_name):
    if not first_name or not first_name.strip():
        return "Enter a first name."
    first_name = first_name.strip().lower()
    found = []
    for mod, (df, _) in loaded_module_dfs.items():
        for col in ['firstName', 'Forename', 'First name']:
            if col in df.columns and df[col].astype(str).str.lower().str.contains(first_name, na=False).any():
                found.append(mod)
                break
    return f"Found in: {', '.join(found)}" if found else "No matches found."


def update_date_dropdowns(module):
    if module in ["Y5R1", "Y3R1", "Y4R1"]:
        return gr.update(choices=["N/A"], value="N/A"), gr.update(choices=["N/A"], value="N/A"), "Rotation data – no dates."

    if module not in loaded_module_dfs:
        return gr.update(choices=["No data"]), gr.update(choices=["No data"]), "Module not loaded."

    df, _ = loaded_module_dfs[module]

    if df.empty:
        return gr.update(choices=["No dates"]), gr.update(choices=["No dates"]), "No dates available."

    min_date = df['startDateTime'].min().date()
    max_date = df['startDateTime'].max().date()

    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    date_strings = date_range.strftime('%Y-%m-%d').tolist()

    default_start = date_strings[0] if date_strings else "No dates"
    default_end = date_strings[-1] if date_strings else "No dates"

    return (
        gr.update(choices=date_strings, value=default_start),
        gr.update(choices=date_strings, value=default_end),
        f"Dates updated for {module} (full range: {default_start} to {default_end})"
    )


def plot_student_attendance(module, student_selection):
    if module in ["Y5R1", "Y3R1", "Y4R1"]:
        return go.Figure(), "Graph not available for rotation data."
    if not student_selection:
        return go.Figure(), "Select a student first."
    match = re.search(r'\((\d+)\)', student_selection)
    if not match:
        return go.Figure(), "Invalid student selection."
    student_id = match.group(1)
    if module not in loaded_module_dfs:
        return go.Figure(), "Module data not loaded."
    df, _ = loaded_module_dfs[module]
    student_df = df[df['studentId'] == str(student_id)]
    if student_df.empty:
        return go.Figure(), f"No data for student {student_id}."
    student_df = student_df.sort_values('startDateTime')
    student_df['present_num'] = student_df['present'].astype(int)
    student_df['cum_present'] = student_df['present_num'].cumsum()
    student_df['cum_events'] = range(1, len(student_df) + 1)
    student_df['cum_rate'] = (student_df['cum_present'] / student_df['cum_events']) * 100
    overall = df['present'].mean() * 100 if not df.empty else 0
    name = f"{student_df['firstName'].iloc[0]} {student_df['surname'].iloc[0]}"
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=student_df['startDateTime'], y=student_df['cum_rate'], mode='lines+markers', name=f"{name} Attendance", line=dict(color='red')))
    fig.add_trace(go.Scatter(x=[student_df['startDateTime'].min(), student_df['startDateTime'].max()], y=[overall, overall], mode='lines', name=f'Overall Avg ({overall:.2f}%)', line=dict(color='blue', dash='dash')))
    fig.update_layout(title=f"Attendance for {name} in MBCHB{module}", xaxis_title="Date", yaxis_title="Cumulative Attendance (%)", yaxis=dict(range=[0,100]), xaxis=dict(tickangle=45))
    absences = student_df[student_df['present']==False][['eventDescription','startDateTime']]
    absence_text = "No absences." if absences.empty else "Absent Events:\n" + "\n".join(
        f"- {r.eventDescription} on {r.startDateTime.strftime('%Y-%m-%d %H:%M')}" for _,r in absences.iterrows())
    return fig, absence_text


def get_academic_week(date):
    base = datetime(date.year if date.month >= 8 else date.year - 1, 8, 25)
    delta = (date - base).days
    return max(1, delta // 7 + 1)


def get_week_date_range(week, year):
    base = datetime(year if week >= 1 else year - 1, 8, 25)
    week_start = base + timedelta(days=(week - 1) * 7)
    week_end = week_start + timedelta(days=6)
    return f"{week_start.strftime('%d/%m/%Y')}-{week_end.strftime('%d/%m/%Y')}"


def analyze_attendance(module, start_date, end_date, threshold, show_self_cert, sort_order, secondary_sort_by_surname, placement_sort):
    global loaded_notes_df
    if start_date is None or "N/A" in str(start_date) or "No dates" in str(start_date):
        return "Please select a module and valid date range.", "<p>Select valid dates.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>", "<p>No placement absences data.</p>"

    if module in ["Y5R1", "Y3R1", "Y4R1"]:
        rot_key = "Y4R1" if module == "Y4R1" else module
        if rot_key not in loaded_rotation_maps or not loaded_rotation_maps[rot_key]:
            return "Rotation data not loaded.", "<p>No data.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>", "<p>No placement data.</p>"
        df = pd.DataFrame.from_dict(loaded_rotation_maps[rot_key], orient='index')
        df = df.reset_index().rename(columns={'index': 'Student ID'})
        df = df.merge(loaded_notes_df, left_on='Student ID', right_on='studentId', how='left').fillna({'studentEmail': '', 'notes': ''})
        student_table_html = df[['Student ID', 'studentEmail', 'Group', 'rotation' if 'rotation' in df.columns else 'Pattern', 'notes']] \
            .rename(columns={'studentEmail': 'Student Email', 'notes': 'Notes'}).to_html(index=False)
        group_summary = df.groupby('Group').size().reset_index(name='Student Count').to_html(index=False)
        table_html = f"<h3>Year {module[1] if module != 'Y4R1' else '4'} Rotation Summary</h3>{group_summary}<br><h3>Student Details</h3>{student_table_html}"
        return "Rotation data loaded.", table_html, "", gr.update(choices=[], value=None), None, "<p>Rotation data loaded.</p>", "<p>No absences for rotation view.</p>"

    if module not in loaded_module_dfs:
        return "Module data not loaded.", "<p>No data.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>", "<p>No placement data.</p>"

    df, _ = loaded_module_dfs[module]

    try:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)
    except:
        return "Invalid date format.", "<p>Please select valid dates.</p>", "", gr.update(choices=[], value=None), None, "<p>No data.</p>", "<p>No data.</p>"

    filtered = df[df['startDateTime'].between(start_dt, end_dt)]
    if filtered.empty:
        return "No events in selected date range.", "<p>No events in selected date range.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>", "<p>No placement absences.</p>"

    all_students = df[['studentId', 'firstName', 'surname', 'academicAdvisor']].drop_duplicates('studentId')
    all_students['studentId'] = all_students['studentId'].astype(str)

    # Non-placement attendance
    non_med = filtered[~filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False) &
                       ~filtered['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False)]
    if not non_med.empty:
        att_actual = non_med.groupby('studentId')['present'].mean().reset_index(name='present')
        att_actual['attendance_percentage'] = att_actual['present'] * 100
        att_actual['studentId'] = att_actual['studentId'].astype(str)
    else:
        att_actual = pd.DataFrame(columns=['studentId', 'present', 'attendance_percentage'])

    att = all_students.merge(att_actual[['studentId', 'attendance_percentage']], on='studentId', how='left')
    att['attendance_percentage'] = att['attendance_percentage'].fillna(100.0)

    try:
        thresh_val = float(threshold)
    except:
        thresh_val = 50.0

    below = att[att['attendance_percentage'] <= thresh_val]

    if show_self_cert:
        selfcert = filtered[filtered['selfCertInfo'] == True]['studentId'].unique()
        below = below[below['studentId'].isin(selfcert)]

    if not below.empty:
        below = below.merge(loaded_notes_df, left_on='studentId', right_on='studentId', how='left') \
                    .fillna({'notes': '', 'studentEmail': ''})

    ascending = (sort_order == "Lowest to Highest")
    below = below.sort_values(by='attendance_percentage', ascending=ascending)

    if secondary_sort_by_surname:
        below = below.sort_values(by=['surname', 'firstName'], ascending=True).reset_index(drop=True)

    count_html = f"<p><strong>{len(below)} record(s) found.</strong></p>"
    table_html = "<p>No students below threshold.</p>" if below.empty else (
        count_html + below.rename(columns={
            'studentId': 'Student ID',
            'firstName': 'First Name',
            'surname': 'Surname',
            'studentEmail': 'Student Email',
            'attendance_percentage': 'Attendance (%)'
        }).drop(columns=['present', 'academicAdvisor', 'notes'], errors='ignore')
          .round(2)
          .to_html(index=False)
    )

    student_choices = [f"{r['firstName']} {r['surname']} ({r['studentId']})" for _, r in below.iterrows()]

    # ────────────────────────────────────────────────────────────────
    # Placement Analysis – always show all students
    placement_attended_html = "<p>No placement attendance data in selected range.</p>"

    is_clinical = module.startswith(('2','3','4','5'))
    rotation_map = None
    year_label = None
    expected_text = ""

    if module.startswith('5'):
        rotation_map = loaded_rotation_maps.get("Y5R1", {})
        year_label = "5"
        expected_text = "Group 1 Expected: 4 days/week | Group 2 Expected: 3 days/week"
    elif module.startswith('3'):
        rotation_map = loaded_rotation_maps.get("Y3R1", {})
        year_label = "3"
        expected_text = "Group 1 Expected: 2 days/week | Group 2 Expected: 1 day/week"
    elif module.startswith('4'):
        rotation_map = loaded_rotation_maps.get("Y4R1", {})
        year_label = "4"
        expected_text = "Group 1 Expected: 3 days/week (assumed)"
    elif module.startswith('2'):
        rotation_map = loaded_rotation_maps.get("Y2", {})
        year_label = "2"
        expected_text = "Patterns from y2r*.csv: varies"

    med = filtered[
        (filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)) &
        ~filtered['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False) &
        (filtered['present'] == True)
    ].copy()

    if is_clinical:
        if med.empty:
            # No present placements at all → show all students with 0
            placement_df = all_students.copy()
            placement_df['Group'] = placement_df['studentId'].map(
                lambda sid: rotation_map.get(str(sid), {}).get('hospital', 'Unknown') if year_label == "2" else
                f"Group {rotation_map.get(str(sid), {}).get('group', 'N/A')}" if year_label in ["3","4"] else
                rotation_map.get(str(sid), {}).get('rotation', 'Unknown') if year_label == "5" else 'N/A'
            )
            placement_df['Pattern'] = placement_df['studentId'].map(
                lambda sid: rotation_map.get(str(sid), {}).get('pattern', 'N/A') if year_label == "2" else
                f"{rotation_map.get(str(sid), {}).get('expected_days', 'N/A')} days/week" if year_label in ["3","4","5"] else 'N/A'
            )
            placement_df['Total_Days_Attended'] = 0
            placement_df['Med.Plac Dates'] = "None found"
            placement_df['Week_Range'] = "None"
        else:
            # Some present placements → compute normally, then right-merge with all_students
            med['week'] = med['startDateTime'].apply(get_academic_week)
            med['date'] = med['startDateTime'].dt.date

            weekly_days = pd.DataFrame()
            for sid in med['studentId'].unique():
                student_data = med[med['studentId'] == sid].copy()
                rot_info = rotation_map.get(str(sid), {})
                if year_label == "2":
                    group_label = rot_info.get('hospital', 'Unknown')
                    pattern_label = rot_info.get('pattern', 'N/A')
                elif year_label == "5":
                    group_label = rot_info.get('rotation', 'Unknown')
                    pattern_label = f"{rot_info.get('expected_days', 'N/A')} days/week"
                elif year_label in ["3","4"]:
                    g = rot_info.get('group')
                    group_label = f"Group {g}" if g is not None else 'Unknown'
                    pattern_label = f"{rot_info.get('expected_days', 'N/A')} days/week"
                else:
                    group_label = pattern_label = 'N/A'

                student_weekly = student_data.groupby(
                    ['studentId','firstName','surname','week']
                )['date'].nunique().reset_index(name='Days_Attended')
                student_weekly['Period_Label'] = student_weekly['week'].apply(
                    lambda w: get_week_date_range(w, start_dt.year if start_dt.month >= 8 else start_dt.year - 1)
                )
                student_weekly['Group'] = group_label
                student_weekly['Pattern'] = pattern_label
                weekly_days = pd.concat([weekly_days, student_weekly], ignore_index=True)

            all_placement = weekly_days.groupby(
                ['studentId', 'firstName', 'surname', 'Group', 'Pattern']
            ).agg(
                Total_Days_Attended=('Days_Attended', 'sum'),
                Week_Range=('Period_Label', lambda x: ', '.join(sorted(set(x))))
            ).reset_index()

            dates_agg = med.groupby('studentId', as_index=False)['startDateTime'].agg(
                lambda x: ', '.join(sorted(set(x.dt.strftime('%Y-%m-%d'))))
            ).rename(columns={'startDateTime': 'Med.Plac Dates'})

            all_placement = all_placement.merge(dates_agg, on='studentId', how='left')
            all_placement['Med.Plac Dates'] = all_placement['Med.Plac Dates'].fillna('None found')

            # RIGHT MERGE → include all students, even those with 0
            placement_df = all_students.merge(
                all_placement,
                on=['studentId', 'firstName', 'surname'],
                how='left'
            ).fillna({
                'Total_Days_Attended': 0,
                'Med.Plac Dates': 'None found',
                'Week_Range': 'None',
                'Group': 'N/A',
                'Pattern': 'N/A'
            })

        placement_df = placement_df.merge(loaded_notes_df, left_on='studentId', right_on='studentId', how='left') \
                                  .fillna({'studentEmail': ''})

        placement_df = placement_df.rename(columns={
            'studentId': 'Student ID',
            'firstName': 'First Name',
            'surname': 'Surname',
            'studentEmail': 'Student Email'
        })[['Student ID', 'First Name', 'Surname', 'Group', 'Pattern', 'Student Email', 'Med.Plac Dates', 'Week_Range', 'Total_Days_Attended']]

        ascending_placement = (placement_sort == "Least Placement Days First")
        placement_df = placement_df.sort_values(by='Total_Days_Attended', ascending=ascending_placement)

        if year_label == "5":
            header = (
                "<h3>Year 5 Medical Placement Attendance – Only PRESENT days</h3>"
                f"<p><strong>{expected_text}</strong></p>"
                "<p><small>Note: Only counts days with at least one present=True check-in (MED.PLAC or MED.OTHR) – MED.STUDY excluded<br>"
                "All students shown – 0 if no qualifying present check-ins.</small></p>"
            )
        elif year_label == "3":
            header = (
                "<h3>Year 3 Medical Placement Attendance – Only PRESENT days</h3>"
                f"<p><strong>{expected_text}</strong></p>"
                "<p><small>Note: Only counts days with at least one present=True check-in (MED.PLAC or MED.OTHR) – MED.STUDY excluded<br>"
                "All students shown – 0 if no qualifying present check-ins.</small></p>"
            )
        elif year_label == "4":
            header = (
                "<h3>Year 4 Medical Placement Attendance – Only PRESENT days</h3>"
                f"<p><strong>{expected_text}</strong></p>"
                "<p><small>Note: Only counts days with at least one present=True check-in (MED.PLAC or MED.OTHR) – MED.STUDY excluded<br>"
                "All students shown – 0 if no qualifying present check-ins.</small></p>"
            )
        else:
            header = (
                "<h3>Year 2 Medical Placement Attendance – Only PRESENT days</h3>"
                f"<p><strong>{expected_text}</strong></p>"
                "<p><small>Note: Only counts days with at least one present=True check-in (MED.PLAC or MED.OTHR) – MED.STUDY excluded<br>"
                "All students shown – 0 if no qualifying present check-ins.</small></p>"
            )

        placement_attended_html = header + placement_df.to_html(index=False)

    else:
        # Year 1 / non-clinical
        placement_attended_html = "<p>Placement analysis not applicable for this module (pre-clinical / Year 1).</p>"

    # ────────────────────────────────────────────────────────────────
    # Placement absences table (Self-Cert / Cancelled)
    medplac_html = "<p>No explicit placement absences in selected range.</p>"

    med_abs = filtered[
        (filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)) &
        ~filtered['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False) &
        (filtered['present'] == False)
    ]

    if not med_abs.empty:
        medplac_df = med_abs[['studentId', 'firstName', 'surname', 'eventDescription', 'startDateTime']].copy()
        medplac_df['Date'] = medplac_df['startDateTime'].dt.strftime('%Y-%m-%d %H:%M')

        if is_clinical and rotation_map:
            def get_group(sid_str):
                info = rotation_map.get(str(sid_str), {})
                if year_label == "5":
                    return info.get('rotation', 'Unknown')
                elif year_label in ["3", "4"]:
                    g = info.get('group')
                    return f"Group {g}" if g is not None else 'Unknown'
                elif year_label == "2":
                    return info.get('hospital', 'Unknown')
                return 'N/A'

            medplac_df['Group'] = medplac_df['studentId'].astype(str).map(get_group)
            cols = ['Student ID','First Name','Surname','Group','Student Email','Event Description','Date','Notes']
        else:
            medplac_df['Group'] = 'N/A'
            cols = ['Student ID','First Name','Surname','Student Email','Event Description','Date','Notes']

        medplac_df = medplac_df.merge(loaded_notes_df, left_on='studentId', right_on='studentId', how='left') \
                               .fillna({'notes': '', 'studentEmail': ''})
        medplac_df = medplac_df.rename(columns={
            'studentId': 'Student ID',
            'firstName': 'First Name',
            'surname': 'Surname',
            'studentEmail': 'Student Email',
            'eventDescription': 'Event Description',
            'notes': 'Notes'
        })

        title = "Self-Cert / Cancelled Check In (present=False)" + (" – Year 1" if not is_clinical else "")
        medplac_html = f"<h3>{title}</h3>" + medplac_df[cols].to_html(index=False)

    return (
        "Analysis complete.",
        table_html,
        "",
        gr.update(choices=student_choices, value=None),
        None,
        placement_attended_html,
        medplac_html
    )


def macro_attendance(module, days_back):
    global loaded_notes_df
    if module not in loaded_module_dfs:
        return "<p>Module not loaded.</p>"

    df, _ = loaded_module_dfs[module]
    cutoff = datetime.now() - timedelta(days=days_back)

    # Get all students from the full dataset (so we always have names)
    all_students = df[['studentId', 'firstName', 'surname']].drop_duplicates('studentId')
    all_students['studentId'] = all_students['studentId'].astype(str)

    med_events = df[
        df['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False) &
        ~df['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False) &
        (df['startDateTime'] >= cutoff)
    ].copy()

    if med_events.empty:
        # No placement events → show all students with 0 count
        counts = all_students.copy()
        counts['Placement_Count'] = 0
    else:
        med_events['date'] = med_events['startDateTime'].dt.date
        med_events['studentId'] = med_events['studentId'].astype(str)

        max_per_day = 2 if module.startswith(('2','3','4','5')) else 999

        capped = med_events.groupby(['studentId', 'date']).size().reset_index(name='daily_count')
        capped['capped_count'] = capped['daily_count'].clip(upper=max_per_day)
        counts_from_events = capped.groupby('studentId')['capped_count'].sum().reset_index(name='Placement_Count')

        # Right-merge with all_students so everyone appears (0 if missing)
        counts = all_students.merge(counts_from_events, on='studentId', how='left')
        counts['Placement_Count'] = counts['Placement_Count'].fillna(0)

    # Add rotation/group/pattern info
    rotation_map = loaded_rotation_maps.get(
        "Y5R1" if module.startswith('5') else
        "Y3R1" if module.startswith('3') else
        "Y4R1" if module.startswith('4') else
        "Y2", {}
    )

    if module.startswith('2'):
        counts['Group'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('hospital', 'N/A'))
        counts['Pattern'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('pattern', 'N/A'))
    elif module.startswith('3'):
        counts['Group'] = counts['studentId'].map(lambda sid: f"Group {rotation_map.get(sid, {}).get('group', 'N/A')}")
        counts['Pattern'] = counts['studentId'].map(lambda sid: f"{rotation_map.get(sid, {}).get('expected_days', 'N/A')} days/week")
    elif module.startswith('4'):
        counts['Group'] = counts['studentId'].map(lambda sid: f"Group {rotation_map.get(sid, {}).get('group', 'N/A')}")
        counts['Pattern'] = counts['studentId'].map(lambda sid: f"{rotation_map.get(sid, {}).get('expected_days', 'N/A')} days/week")
    elif module.startswith('5'):
        counts['Group'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('rotation', 'N/A'))
        counts['Pattern'] = counts['studentId'].map(lambda sid: f"{rotation_map.get(sid, {}).get('expected_days', 'N/A')} days/week")
    else:
        counts['Group'] = counts['Pattern'] = 'N/A'

    counts = counts.merge(loaded_notes_df, left_on='studentId', right_on='studentId', how='left') \
                  .fillna({'studentEmail': ''})

    counts = counts.sort_values('Placement_Count')

    table = counts.rename(columns={
        'studentId': 'Student ID',
        'firstName': 'First Name',
        'surname': 'Surname',
        'studentEmail': 'Student Email',
        'Group': 'Group/Rotation',
        'Pattern': 'Pattern',
        'Placement_Count': f'Placement Events (Last {days_back} days, capped)'
    })[['Student ID', 'First Name', 'Surname', 'Student Email', 'Group/Rotation', 'Pattern', f'Placement Events (Last {days_back} days, capped)']].to_html(index=False, escape=False)

    max_per_day = 2 if module.startswith(('2','3','4','5')) else 999
    header = f"""
    <h3>Placement Attendance Macro View – Last {days_back} days</h3>
    <p><small>(includes both MED.PLAC and MED.OTHR – daily cap: {max_per_day} for clinical years; MED.STUDY excluded)<br>
    All students shown – 0 if no qualifying check-ins in period.</small></p>
    """

    return header + table


def self_certified_events(module, start_date, end_date):
    global loaded_notes_df
    if module not in loaded_module_dfs:
        return "<p>Module not loaded. Please load data first.</p>"
    if start_date is None or "N/A" in str(start_date) or end_date is None or "N/A" in str(end_date):
        return "<p>Please select valid start and end dates.</p>"

    df, _ = loaded_module_dfs[module]

    try:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)
    except:
        return "<p>Invalid date format. Please select dates from the dropdowns.</p>"

    filtered = df[df['startDateTime'].between(start_dt, end_dt)].copy()
    if filtered.empty:
        return "<p>No events found in the selected date range.</p>"

    if 'registerType' not in filtered.columns:
        return "<p>No 'registerType' column found in data.</p>"

    selfcert_df = filtered[filtered['registerType'] == '50'].copy()
    if selfcert_df.empty:
        return "<p>No self-certified events (registerType=50) found in selected date range.</p>"

    selfcert_df = selfcert_df[~selfcert_df['eventDescription'].str.contains(SELF_STUDY_PATTERNS, na=False)]
    if selfcert_df.empty:
        return "<p>No qualifying self-certified events after excluding self-study/med.study.</p>"

    selfcert_df['date'] = selfcert_df['startDateTime'].dt.date
    selfcert_df['studentId'] = selfcert_df['studentId'].astype(str)

    is_placement = selfcert_df['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)
    placement_self = selfcert_df[is_placement].copy()
    non_placement_self = selfcert_df[~is_placement].copy()

    counted_events = []
    if not placement_self.empty:
        daily = placement_self.groupby(['studentId', 'date']).size().reset_index(name='daily_count')
        daily['counted'] = daily['daily_count'].clip(upper=2)
        daily = daily[daily['counted'] > 0]
        for _, row in daily.iterrows():
            sid = row['studentId']
            dt = row['date']
            cnt = row['counted']
            counted_events.extend([(sid, dt)] * cnt)

    if not non_placement_self.empty:
        for _, row in non_placement_self.iterrows():
            sid = row['studentId']
            dt = row['date']
            counted_events.append((sid, dt))

    if not counted_events:
        return "<p>No counted self-certified events after applying rules.</p>"

    counted_df = pd.DataFrame(counted_events, columns=['studentId', 'date'])
    summary = counted_df.groupby('studentId').agg(
        Count=('date', 'size'),
        Dates=('date', lambda x: ', '.join(x.astype(str).sort_values()))
    ).reset_index()

    names = filtered[['studentId', 'firstName', 'surname']].drop_duplicates('studentId')
    summary = summary.merge(names, on='studentId', how='left')
    summary = summary.merge(loaded_notes_df[['studentId', 'studentEmail']], on='studentId', how='left') \
                     .fillna({'firstName': '', 'surname': '', 'studentEmail': ''})

    summary = summary.sort_values(by=['Count', 'surname'], ascending=[False, True])

    final = summary[['studentId', 'firstName', 'surname', 'studentEmail', 'Dates', 'Count']].rename(columns={
        'studentId': 'Student ID',
        'firstName': 'First Name',
        'surname': 'Surname',
        'studentEmail': 'Student Email',
        'Dates': 'Self-Cert Dates (counted)',
        'Count': 'Count'
    })

    header = (
        "<h3>Self-Certified Events</h3>"
        "<p><strong>Counting rules:</strong> All registerType=50 events (ignores present value). "
        "Excludes MED.STUDY / self-study events. "
        "Placement events (MED.PLAC, MED.OTHR, palliative care): max 2 counted per student per day. "
        "Non-placement events: no daily limit. "
        "Time window: selected date range. "
        "<br><strong>Placement check-ins within 10 minutes are deduplicated (treated as one event).</strong></p>"
    )

    if final.empty:
        return header + "<p>No self-certified events to display.</p>"

    table = final.to_html(index=False, escape=False)
    return header + f"<p><strong>{len(final)} student(s) with counted self-cert events.</strong></p>" + table


with gr.Blocks() as demo:
    gr.Markdown("# MBChB Attendance Analysis Dashboard")
    gr.Markdown("Upload files below, then click 'Load / Refresh Data'")
    with gr.Row():
        book1_upload = gr.File(label="Book1.xlsx (notes & emails)", file_types=[".xlsx"])
        y5_upload = gr.File(label="Year 5 rotations (y5r*.csv – multiple allowed)", file_types=[".csv"], file_count="multiple")
        y3_upload = gr.File(label="Year 3 rotations (y3r*.csv – multiple allowed)", file_types=[".csv"], file_count="multiple")
        y4_upload = gr.File(label="Year 4 rotations (y4r*.csv – multiple allowed)", file_types=[".csv"], file_count="multiple")
        y2_upload = gr.File(label="Year 2 rotations (y2r*.csv – multiple allowed)", file_types=[".csv"], file_count="multiple")
        module_uploads = gr.File(label="Attendance log files (lusi_mbchb*.csv) – multiple allowed", file_types=[".csv"], file_count="multiple")

    load_btn = gr.Button("Load / Refresh Data", variant="primary")
    load_status = gr.Textbox(label="Loading Status", lines=5)
    module_dd = gr.Dropdown(label="Select Module", choices=[], interactive=True)

    with gr.Row():
        student_search = gr.Textbox(label="Find Student by First Name")
        search_btn = gr.Button("Search")

    search_result = gr.Textbox(label="Search Result", lines=3)

    with gr.Row():
        start_date_dd = gr.Dropdown(label="Start Date")
        end_date_dd = gr.Dropdown(label="End Date")

    with gr.Row():
        thresh_number = gr.Number(
            label="Threshold (%) – show students ≤ this value (decimals allowed)",
            value=50.0, minimum=0.0, maximum=100.0, step=0.0001, precision=6
        )
        sort_dd = gr.Dropdown(choices=["Lowest to Highest", "Highest to Lowest"], label="Sort Attendance", value="Lowest to Highest")
        sec_sort_cb = gr.Checkbox(label="Also sort by surname (A–Z)", value=True)

    with gr.Row():
        plac_sort_dd = gr.Dropdown(choices=["Least Placement Days First", "Most Placement Days First"], label="Sort Placement", value="Least Placement Days First")
        self_cert_cb = gr.Checkbox(label="Show only self-certified absences", value=False)

    analyze_btn = gr.Button("Analyze Attendance", variant="primary")
    status_out = gr.Textbox(label="Status", lines=3)

    with gr.Tab("Attendance Summary"):
        summary_table = gr.HTML()

    with gr.Tab("Student Details"):
        student_radio = gr.Radio(label="Select Student", choices=[])
        attendance_graph = gr.Plot()
        absence_text = gr.Textbox(label="Absent Events", lines=8)

    with gr.Tab("Placement Analysis"):
        placement_table = gr.HTML()

    with gr.Tab("Self-Cert Placement"):
        self_cert_placement_table = gr.HTML()

    with gr.Tab("Attendance Macro"):
        days_slider = gr.Slider(7, 365, value=30, step=1, label="Look back X days")
        macro_btn = gr.Button("Refresh Macro View")
        macro_table = gr.HTML()

    with gr.Tab("Self-Certified Events"):
        self_cert_refresh = gr.Button("Refresh Self-Cert View", variant="primary")
        self_cert_table = gr.HTML()

    load_btn.click(
        load_all_files,
        inputs=[book1_upload, y5_upload, y3_upload, y4_upload, y2_upload, module_uploads],
        outputs=[load_status, module_dd]
    )

    module_dd.change(
        update_date_dropdowns,
        inputs=module_dd,
        outputs=[start_date_dd, end_date_dd, status_out]
    )

    search_btn.click(
        find_student,
        inputs=student_search,
        outputs=search_result
    )

    analyze_btn.click(
        analyze_attendance,
        inputs=[module_dd, start_date_dd, end_date_dd, thresh_number, self_cert_cb, sort_dd, sec_sort_cb, plac_sort_dd],
        outputs=[status_out, summary_table, absence_text, student_radio, attendance_graph, placement_table, self_cert_placement_table]
    )

    student_radio.change(
        plot_student_attendance,
        inputs=[module_dd, student_radio],
        outputs=[attendance_graph, absence_text]
    )

    macro_btn.click(
        macro_attendance,
        inputs=[module_dd, days_slider],
        outputs=macro_table
    )

    self_cert_refresh.click(
        self_certified_events,
        inputs=[module_dd, start_date_dd, end_date_dd],
        outputs=self_cert_table
    )

    gr.Markdown(
        "**Instructions:** Upload files first, click 'Load / Refresh Data', then select a module and analyze.\n\n"
        "**Note:** MED.STUDY and self-study events are excluded from all metrics. "
        "Students with zero qualifying sessions in the selected date range show as 0%.\n"
        "**Placement check-ins within 10 minutes are now treated as a single event.**\n\n"
        "**Updated:** Placement Analysis & Macro tabs now always show **all students** with 0 where no qualifying present events exist."
    )

demo.launch()
