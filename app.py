import gradio as gr
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import os

loaded_module_dfs = {}
loaded_rotation_maps = {"Y5R1": None, "Y3R1": None, "Y2": None, "Y4R1": None}
loaded_notes_df = pd.DataFrame(columns=['studentId', 'studentEmail', 'notes'])

PLACEMENT_PATTERNS = r"(?i)(med\.plac|med\.othr|palliative care)"

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
        df['selfCertInfo'] = df.get('selfCertInfo', pd.Series([False] * len(df), index=df.index))
        df['cancelled'] = df.get('cancelled', pd.Series([False] * len(df), index=df.index))
        df = df[df['cancelled'] == False]
        required = ['studentId', 'firstName', 'surname', 'academicAdvisor', 'startDateTime']
        if not all(col in df.columns for col in required):
            return None, [], "Missing required columns."
        df = df.dropna(subset=required)
        if df.empty:
            return None, [], "No valid data after cleaning."
        unique_dates = sorted(df['startDateTime'].dt.date.astype(str).unique())
        return df, unique_dates, f"Loaded {len(df)} rows from {os.path.basename(file_path)}"
    except Exception as e:
        return None, [], f"Error loading file: {str(e)}"

def parse_pattern_to_days(pattern):
    if pd.isna(pattern) or not isinstance(pattern, str):
        return None
    match = re.search(r'(\d+)', pattern)
    if match:
        return int(match.group(1))
    return None

def load_y5_rotation_data(file_path):
    global loaded_rotation_maps
    if not file_path or not os.path.exists(file_path):
        return "y5r1.csv not uploaded."
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df['Student ID'] = df['Student ID'].astype(str).str.strip()
        rotation_map = {}
        for q, row in df.iterrows():
            sid = str(row['Student ID'])
            group = int(row.get('Group', 1))
            pattern = row.get('Pattern', row.get('pattern', 'N/A')).strip()
            expected_days = parse_pattern_to_days(pattern)
            rotation_map[sid] = {
                'group': group,
                'expected_days': expected_days,
                'pattern': pattern,
                'rotation': row.get('Rotation 1', 'Unknown')
            }
        loaded_rotation_maps["Y5R1"] = rotation_map
        return "y5r1.csv loaded successfully."
    except Exception as e:
        return f"Error loading y5r1.csv: {str(e)}"

def load_y3_rotation_data(file_path):
    global loaded_rotation_maps
    if not file_path or not os.path.exists(file_path):
        return "y3r1.csv not uploaded."
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df['Student ID'] = df['Student ID'].astype(str).str.strip()
        rotation_map = {}
        for q, row in df.iterrows():
            sid = str(row['Student ID'])
            group = int(row.get('Group', 2))
            pattern = row.get('Pattern', row.get('pattern', 'N/A')).strip()
            expected_days = parse_pattern_to_days(pattern)
            rotation_map[sid] = {
                'group': group,
                'expected_days': expected_days,
                'pattern': pattern,
                'rotation': row.get('Pattern', 'N/A')
            }
        loaded_rotation_maps["Y3R1"] = rotation_map
        return "y3r1.csv loaded successfully."
    except Exception as e:
        return f"Error loading y3r1.csv: {str(e)}"

def load_y4_rotation_data(file_path):
    global loaded_rotation_maps
    if not file_path or not os.path.exists(file_path):
        return "y4r1.csv not uploaded."
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df_key = 'student_id' if 'student_id' in df.columns else 'Student ID'
        df[df_key] = df[df_key].astype(str).str.strip()
        rotation_map = {}
        for q, row in df.iterrows():
            sid = str(row[df_key])
            group = int(row.get('Group', 1))
            pattern = row.get('Pattern', row.get('pattern', 'N/A')).strip()
            expected_days = parse_pattern_to_days(pattern)
            rotation_map[sid] = {
                'group': group,
                'expected_days': expected_days,
                'pattern': pattern,
                'rotation': row.get('Pattern', 'N/A')
            }
        loaded_rotation_maps["Y4R1"] = rotation_map
        return "y4r1.csv loaded successfully."
    except Exception as e:
        return f"Error loading y4r1.csv: {str(e)}"

def load_y2_rotation_data(file_path):
    global loaded_rotation_maps
    if not file_path or not os.path.exists(file_path):
        return "y2r1.csv not uploaded."
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
        df.columns = df.columns.str.strip()
        df['Student No.'] = df['Student No.'].astype(str).str.strip()
        rotation_map = {}
        for q, row in df.iterrows():
            sid = str(row['Student No.'])
            trust = row.get('Trust (B1)', 'Unknown').strip().upper()
            pattern = row.get('pattern', 'N/A').strip()
            expected_days = parse_pattern_to_days(pattern)
            rotation_map[sid] = {
                'hospital': trust,
                'pattern': pattern,
                'expected_days': expected_days
            }
        loaded_rotation_maps["Y2"] = rotation_map
        return "y2r1.csv loaded successfully."
    except Exception as e:
        return f"Error loading y2r1.csv: {str(e)}"

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


def load_all_files(book1_file, y5_file, y3_file, y4_file, y2_file, module_files):
    global loaded_module_dfs
    loaded_module_dfs.clear()
    messages = []
    messages.append(load_notes(book1_file))
    messages.append(load_y5_rotation_data(y5_file))
    messages.append(load_y3_rotation_data(y3_file))
    messages.append(load_y4_rotation_data(y4_file))
    messages.append(load_y2_rotation_data(y2_file))
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
    if loaded_rotation_maps["Y5R1"]:
        available_modules.append("Y5R1")
    if loaded_rotation_maps["Y3R1"]:
        available_modules.append("Y3R1")
    if loaded_rotation_maps["Y4R1"]:
        available_modules.append("Y4R1")
    if not available_modules:
        available_modules = ["No modules loaded – upload at least one lusi_mbchb*.csv or rotation file"]
    return "\n".join(messages), gr.update(choices=available_modules), "Files loaded. Select a module to analyze."

def find_student(first_name):
    if not first_name or not first_name.strip():
        return "Enter a first name."
    first_name = first_name.strip().lower()
    found = []
    for mod, (df, x) in loaded_module_dfs.items():
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
    x, dates = loaded_module_dfs[module]
    if not dates:
        return gr.update(choices=["No dates"]), gr.update(choices=["No dates"]), "No dates available."
    return gr.update(choices=dates, value=dates[0]), gr.update(choices=dates, value=dates[-1]), f"Dates updated for {module}"

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
    df, x = loaded_module_dfs[module]
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
    absence_text = "No absences." if absences.empty else "Absent Events:\n" + "\n".join(f"- {r.eventDescription} on {r.startDateTime.strftime('%Y-%m-%d %H:%M')}" for _,r in absences.iterrows())
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
    notes_grouped = loaded_notes_df
    if start_date is None or "N/A" in str(start_date) or "No dates" in str(start_date):
        return "Please select a module and valid date range.", "<p>Select valid dates.</p>", "", gr.update(choices=[], value=None), None, "<p>No data.</p>"
    if module in ["Y5R1", "Y3R1", "Y4R1"]:
        rot_key = "Y4R1" if module == "Y4R1" else module
        if rot_key not in loaded_rotation_maps or not loaded_rotation_maps[rot_key]:
            return "Rotation data not loaded.", "<p>No data.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>"
        df = pd.DataFrame.from_dict(loaded_rotation_maps[rot_key], orient='index')
        df = df.reset_index().rename(columns={'index': 'Student ID'})
        df = df.merge(notes_grouped, left_on='Student ID', right_on='studentId', how='left').fillna({'studentEmail': '', 'notes': ''})
        student_table_html = df[['Student ID', 'studentEmail', 'Group', 'rotation' if 'rotation' in df.columns else 'Pattern', 'notes']].rename(
            columns={'studentEmail': 'Student Email', 'notes': 'Notes'}
        ).to_html(index=False)
        group_summary = df.groupby('Group').size().reset_index(name='Student Count').to_html(index=False)
        table_html = f"<h3>Year {module[1] if module != 'Y4R1' else '4'} Rotation Summary</h3>{group_summary}<br><h3>Student Details</h3>{student_table_html}"
        return "Rotation data loaded.", table_html, "", gr.update(choices=[], value=None), None, "<p>Rotation data loaded.</p>"
    if module not in loaded_module_dfs:
        return "Module data not loaded.", "<p>No data.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>"
    df, x = loaded_module_dfs[module]
    try:
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date) + timedelta(days=1) - timedelta(seconds=1)
    except:
        return "Invalid date format.", "<p>Please select valid dates.</p>", "", gr.update(choices=[], value=None), None, "<p>No data.</p>"
    filtered = df[df['startDateTime'].between(start_dt, end_dt)]
    if filtered.empty:
        return "No events in selected date range.", "<p>No events in selected date range.</p>", "", gr.update(choices=[], value=None), None, "<p>No placement data.</p>"
    rotation_map = loaded_rotation_maps.get("Y5R1" if module.startswith('5') else "Y3R1" if module.startswith('3') else "Y4R1" if module.startswith('4') else "Y2", {})
    non_med = filtered[~filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)]
    att = non_med.groupby(['studentId', 'firstName', 'surname', 'academicAdvisor'])['present'].mean().reset_index()
    att['attendance_percentage'] = att['present'] * 100
    below = att[att['attendance_percentage'] < float(threshold)]
    if show_self_cert:
        selfcert = filtered[filtered['selfCertInfo'] == True]['studentId'].unique()
        below = below[below['studentId'].isin(selfcert)]
    if not below.empty:
        below = below.merge(notes_grouped, left_on='studentId', right_on='studentId', how='left').fillna({'notes': '', 'studentEmail': ''})
        ascending = (sort_order == "Lowest to Highest")
        below = below.sort_values(by='attendance_percentage', ascending=ascending)
        if secondary_sort_by_surname:
            below = below.sort_values(by=['surname', 'firstName'], ascending=True).reset_index(drop=True)
    count_html = f"<p><strong>{len(below)} record(s) found.</strong></p>"
    table_html = "<p>No students below threshold.</p>" if below.empty else (
        count_html +
        below.rename(columns={
            'studentId': 'Student ID', 'firstName': 'First Name', 'surname': 'Surname',
            'studentEmail': 'Student Email',
            'attendance_percentage': 'Attendance (%)'
        }).drop(columns=['present', 'academicAdvisor', 'notes']).round(2).to_html(index=False)
    )
    student_choices = [f"{r['firstName']} {r['surname']} ({r['studentId']})" for _, r in below.iterrows()]
    medplac_html = ""
    med_table_html = ""
    if module.startswith(('5','3','2','4')):
        med = filtered[filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)].copy()
        if not med.empty:
            med['week'] = med['startDateTime'].apply(get_academic_week)
            med['date'] = med['startDateTime'].dt.date
            weekly_days = pd.DataFrame()
            for sid in med['studentId'].unique():
                student_data = med[med['studentId'] == sid].copy()
                rot_info = rotation_map.get(str(sid), {})
                if module.startswith('2'):
                    group_label = rot_info.get('hospital', 'Unknown')
                    pattern_label = rot_info.get('pattern', 'N/A')
                elif module.startswith('5'):
                    group_label = rot_info.get('rotation', 'Unknown')
                    pattern_label = rot_info.get('pattern', 'N/A')  
                elif module.startswith('3'):
                    g = rot_info.get('group')
                    group_label = f"Group {g}" if g is not None else 'Unknown'
                    pattern_label = rot_info.get('pattern', 'N/A') 
                elif module.startswith('4'):
                    g = rot_info.get('group')
                    group_label = f"Group {g}" if g is not None else 'Unknown'
                    pattern_label = rot_info.get('pattern', 'N/A')  
                else:
                    group_label = pattern_label = 'N/A'
                student_weekly = student_data.groupby(['studentId','firstName','surname','week'])['date'].nunique().reset_index(name='Days_Attended')
                student_weekly['Period_Label'] = student_weekly['week'].apply(lambda w: get_week_date_range(w, start_dt.year if start_dt.month >= 8 else start_dt.year - 1))
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
            all_placement = all_placement.merge(notes_grouped, left_on='studentId', right_on='studentId', how='left').fillna({'studentEmail': ''})
            ascending_placement = (placement_sort == "Least Placement Days First")
            all_placement = all_placement.sort_values(by='Total_Days_Attended', ascending=ascending_placement)
            all_placement = all_placement.rename(columns={
                'studentId': 'Student ID', 'firstName': 'First Name', 'surname': 'Surname',
                'studentEmail': 'Student Email'
            })[[
                'Student ID', 'First Name', 'Surname', 'Group', 'Pattern',
                'Student Email', 'Med.Plac Dates',
                'Week_Range', 'Total_Days_Attended'
            ]]
            if module.startswith('5'):
                med_table_html = (
                    "<h3>Year 5 Medical Placement Attendance – All Students with ≥1 event</h3>"
                    "<p><small>Note: Counts both automatic (MED.PLAC) and manual (MED.OTHR) placement check-ins</small></p>" +
                    all_placement.to_html(index=False)
                )
            elif module.startswith('3'):
                med_table_html = (
                    "<h3>Year 3 Medical Placement Attendance – All Students with ≥1 event</h3>"
                    "<p><small>Note: Counts both automatic (MED.PLAC) and manual (MED.OTHR) placement check-ins</small></p>" +
                    all_placement.to_html(index=False)
                )
            elif module.startswith('4'):
                med_table_html = (
                    "<h3>Year 4 Medical Placement Attendance – All Students with ≥1 event</h3>"
                    "<p><small>Note: Counts both automatic (MED.PLAC) and manual (MED.OTHR) placement check-ins</small></p>" +
                    all_placement.to_html(index=False)
                )
            else:
                med_table_html = (
                    "<h3>Year 2 Medical Placement Attendance – All Students with ≥1 event</h3>"
                    "<p><small>Note: Counts both automatic (MED.PLAC) and manual (MED.OTHR) placement check-ins</small></p>" +
                    all_placement.to_html(index=False)
                )
            med_abs = filtered[
                (filtered['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False)) &
                (filtered['present'] == False)
            ]
            if not med_abs.empty:
                medplac_df = med_abs[['studentId', 'firstName', 'surname', 'eventDescription', 'startDateTime']].copy()
                medplac_df['Date'] = medplac_df['startDateTime'].dt.strftime('%Y-%m-%d %H:%M')
                def get_group(sid_str):
                    info = rotation_map.get(sid_str, {})
                    if module.startswith('5'):
                        return info.get('rotation', 'Unknown')
                    elif module.startswith('3'):
                        g = info.get('group')
                        return f"Group {g}" if g is not None else 'Unknown'
                    elif module.startswith('4'):
                        g = info.get('group')
                        return f"Group {g}" if g is not None else 'Unknown'
                    elif module.startswith('2'):
                        return info.get('hospital', 'Unknown')
                    return 'N/A'
                medplac_df['Group'] = medplac_df['studentId'].astype(str).map(get_group)
                medplac_df = medplac_df.merge(notes_grouped, left_on='studentId', right_on='studentId', how='left').fillna({'notes': '', 'studentEmail': ''})
                medplac_df = medplac_df.rename(columns={
                    'studentId': 'Student ID', 'firstName': 'First Name', 'surname': 'Surname',
                    'studentEmail': 'Student Email', 'eventDescription': 'Event Description', 'notes': 'Notes'
                })
                medplac_html = (
                    "<h3>Explicit Placement Absences</h3>" +
                    medplac_df[['Student ID', 'First Name', 'Surname', 'Group', 'Student Email', 'Event Description', 'Date', 'Notes']].to_html(index=False)
                )
    full_med_html = (medplac_html + "<br>" + med_table_html) if medplac_html or med_table_html else "<p>No placement data.</p>"
    return "Analysis complete.", table_html, "", gr.update(choices=student_choices, value=None), None, full_med_html

def macro_attendance(module, days_back):
    global loaded_notes_df
    if module not in loaded_module_dfs:
        return "<p>Module not loaded.</p>"
    df, x = loaded_module_dfs[module]
    cutoff = datetime.now() - timedelta(days=days_back)
    med_events = df[
        df['eventDescription'].str.contains(PLACEMENT_PATTERNS, na=False) &
        (df['startDateTime'] >= cutoff)
    ]
    if med_events.empty:
        return f"<p>No placement events (MED.PLAC or MED.OTHR) found in the last {days_back} days.</p>"
    counts = med_events.groupby(['studentId', 'firstName', 'surname']).size().reset_index(name='Placement_Count')
    rotation_map = loaded_rotation_maps.get("Y5R1" if module.startswith('5') else "Y3R1" if module.startswith('3') else "Y4R1" if module.startswith('4') else "Y2", {})
    if module.startswith('2'):
        counts['Group'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('hospital', 'N/A'))
        counts['Pattern'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('pattern', 'N/A'))
    elif module.startswith('3'):
        counts['Group'] = counts['studentId'].map(lambda sid: f"Group {rotation_map.get(sid, {}).get('group', 'N/A')}")
        counts['Pattern'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('pattern', 'N/A'))
    elif module.startswith('4'):
        counts['Group'] = counts['studentId'].map(lambda sid: f"Group {rotation_map.get(sid, {}).get('group', 'N/A')}")
        counts['Pattern'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('pattern', 'N/A'))
    elif module.startswith('5'):
        counts['Group'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('rotation', 'N/A'))
        counts['Pattern'] = counts['studentId'].map(lambda sid: rotation_map.get(sid, {}).get('pattern', 'N/A'))
    else:
        counts['Group'] = counts['Pattern'] = 'N/A'
    counts = counts.merge(loaded_notes_df, left_on='studentId', right_on='studentId', how='left').fillna({'studentEmail': ''})
    counts = counts.sort_values('Placement_Count')
    table = counts.rename(columns={
        'studentId': 'Student ID',
        'firstName': 'First Name',
        'surname': 'Surname',
        'studentEmail': 'Student Email',
        'Group': 'Group/Rotation',
        'Pattern': 'Pattern',
        'Placement_Count': f'Placement Events (Last {days_back} days)'
    })[['Student ID', 'First Name', 'Surname', 'Student Email', 'Group/Rotation', 'Pattern', f'Placement Events (Last {days_back} days)']].to_html(index=False, escape=False)
    header = f"<h3>Placement Attendance Macro View – Last {days_back} days<br><small>(MED.PLAC and MED.OTHR - includes multiple check ins per day)</small></h3>"
    return header + table

with gr.Blocks() as demo:
    gr.Markdown("# MBChB Attendance Analysis Dashboard")
    gr.Markdown("Upload files below, then click 'Load / Refresh Data'")

    with gr.Row():
        book1_upload = gr.File(label="Book1.xlsx (notes & emails)", file_types=[".xlsx"])
        y5_upload = gr.File(label="y5r1.csv (Year 5 rotations)", file_types=[".csv"])
        y3_upload = gr.File(label="y3r1.csv (Year 3 rotations)", file_types=[".csv"])
        y4_upload = gr.File(label="y4r1.csv (Year 4 rotations)", file_types=[".csv"])
        y2_upload = gr.File(label="y2r1.csv (Year 2 rotations)", file_types=[".csv"])

    module_uploads = gr.File(label="Upload attendance log files (lusi_mbchb*.csv) – multiple allowed", file_types=[".csv"], file_count="multiple")

    load_btn = gr.Button("Load / Refresh Data", variant="primary")
    load_status = gr.Textbox(label="Loading Status", lines=5)

    module_dd = gr.Dropdown(label="Select Module", choices=[], interactive=True)

    with gr.Row():
        student_search = gr.Textbox(label="Find Student by First Name")
        search_btn = gr.Button("Search")

    search_result = gr.Textbox(label="Search Result", lines=3)

    start_date_dd = gr.Dropdown(label="Start Date")
    end_date_dd = gr.Dropdown(label="End Date")

    with gr.Row():
        thresh_dd = gr.Dropdown(choices=[str(i) for i in range(10,101,10)] + ["100"], label="Threshold (%)", value="50")
        sort_dd = gr.Dropdown(choices=["Lowest to Highest", "Highest to Lowest"], label="Sort Attendance", value="Lowest to Highest")
        sec_sort_cb = gr.Checkbox(label="Also sort by surname (A–Z)", value=True)
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

    with gr.Tab("Attendance Macro"):
        days_slider = gr.Slider(7, 90, value=30, step=1, label="Look back X days")
        macro_btn = gr.Button("Refresh Macro View")
        macro_table = gr.HTML()

    load_btn.click(load_all_files, inputs=[book1_upload, y5_upload, y3_upload, y4_upload, y2_upload, module_uploads], outputs=[load_status, module_dd])

    module_dd.change(update_date_dropdowns, inputs=module_dd, outputs=[start_date_dd, end_date_dd, status_out])

    search_btn.click(find_student, inputs=student_search, outputs=search_result)

    analyze_btn.click(analyze_attendance, inputs=[module_dd, start_date_dd, end_date_dd, thresh_dd, self_cert_cb, sort_dd, sec_sort_cb, plac_sort_dd], outputs=[status_out, summary_table, absence_text, student_radio, attendance_graph, placement_table])

    student_radio.change(plot_student_attendance, inputs=[module_dd, student_radio], outputs=[attendance_graph, absence_text])

    macro_btn.click(macro_attendance, inputs=[module_dd, days_slider], outputs=macro_table)

    gr.Markdown("**Instructions:** Upload files first, click 'Load / Refresh Data', then select a module and analyze.")

demo.launch()