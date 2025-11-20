import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import json
import io

st.set_page_config(
    page_title="Octa Services - Factory Tracker",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #FFFFFF;
    }
    
    h1 {color: #FFFFFF; font-weight: bold;}
    h2 {color: #EEEEEE;}
    h3 {color: #CCCCCC;}
    
    .stMarkdown, p, label, .stTextInput label, .stSelectbox label, 
    .stTextArea label, .stNumberInput label {
        color: #FFFFFF !important;
    }
    
    .stButton>button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border: 2px solid #FFFFFF;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #CCCCCC;
        border: 2px solid #CCCCCC;
        color: #000000 !important;
    }
    .stButton>button * {
        color: #000000 !important;
    }
    
    .stFormSubmitButton>button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border: 2px solid #FFFFFF;
        font-weight: bold;
    }
    .stFormSubmitButton>button:hover {
        background-color: #CCCCCC;
        border: 2px solid #CCCCCC;
        color: #000000 !important;
    }
    .stFormSubmitButton>button * {
        color: #000000 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1A1A1A;
        color: #FFFFFF;
    }
    [data-testid="stSidebar"] .stMarkdown {
        color: #FFFFFF !important;
    }
    
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stNumberInput>div>div>input {
        background-color: #1A1A1A;
        color: #FFFFFF;
        border: 1px solid #444444;
    }
    
    .stDateInput>div>div>input {
        background-color: #1A1A1A;
        color: #FFFFFF;
        border: 1px solid #444444;
    }
    
    .dataframe {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #FFFFFF;
    }
    [data-testid="stMetricLabel"] {
        color: #CCCCCC;
    }
    
    .stAlert {
        background-color: #1A1A1A;
        color: #FFFFFF;
        border: 1px solid #444444;
    }
    
    .stRadio label {
        color: #FFFFFF !important;
    }
    
    hr {
        border-color: #444444;
    }
    
    .streamlit-expanderHeader {
        background-color: #1A1A1A;
        color: #FFFFFF !important;
    }
    
    .stDownloadButton>button {
        background-color: #FFFFFF;
        color: #000000 !important;
        border: 2px solid #FFFFFF;
        font-weight: bold;
    }
    .stDownloadButton>button:hover {
        background-color: #CCCCCC;
        border: 2px solid #CCCCCC;
        color: #000000 !important;
    }
    .stDownloadButton>button * {
        color: #000000 !important;
    }
    .stDownloadButton>button p {
        color: #000000 !important;
    }
    .stDownloadButton>button span {
        color: #000000 !important;
    }
    [data-testid="stDownloadButton"] button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    [data-testid="stDownloadButton"] button p {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

def show_floating_logos():
    st.markdown("""
        <style>
        @keyframes float {
            0% {
                transform: translateY(100vh) rotate(0deg);
                opacity: 0;
            }
            10% {
                opacity: 1;
            }
            90% {
                opacity: 1;
            }
            100% {
                transform: translateY(-100vh) rotate(360deg);
                opacity: 0;
            }
        }
        
        .floating-logo {
            position: fixed;
            background-image: url('https://octa-solutions.com/storage/media/93fe1245-224d-459b-857e-5bf92ddd87ec.png?s=fb5d46c3ba508cd0a4a97f38ce1fa4c8');
            background-size: contain;
            background-repeat: no-repeat;
            animation: float 5s ease-in;
            z-index: 9999;
            pointer-events: none;
        }
        </style>
        
        <div class="floating-logo" style="left: 5%; width: 60px; height: 60px; animation-delay: 0s;"></div>
        <div class="floating-logo" style="left: 15%; width: 80px; height: 80px; animation-delay: 0.2s;"></div>
        <div class="floating-logo" style="left: 25%; width: 70px; height: 70px; animation-delay: 0.4s;"></div>
        <div class="floating-logo" style="left: 35%; width: 90px; height: 90px; animation-delay: 0.6s;"></div>
        <div class="floating-logo" style="left: 45%; width: 75px; height: 75px; animation-delay: 0.8s;"></div>
        <div class="floating-logo" style="left: 55%; width: 85px; height: 85px; animation-delay: 1s;"></div>
        <div class="floating-logo" style="left: 65%; width: 65px; height: 65px; animation-delay: 1.2s;"></div>
        <div class="floating-logo" style="left: 75%; width: 95px; height: 95px; animation-delay: 1.4s;"></div>
        <div class="floating-logo" style="left: 85%; width: 70px; height: 70px; animation-delay: 1.6s;"></div>
        <div class="floating-logo" style="left: 95%; width: 80px; height: 80px; animation-delay: 1.8s;"></div>
    """, unsafe_allow_html=True)

SITES = ["Faragallah", "Sakr-old", "Sakr-new", "Arab Daily", "National Foods"]

ENGINEERS = [
    "Eng. Reda Abdelazem",
    "Eng. Raafat Assem",
    "Eng. Mohammed Ezzat",
    "Eng. Adel Magdy",
    "Eng. Mohammed Khaled",
    "Eng. Khaled Mostafa",
    "Eng. Ibrahim Elgarhy",
    "Eng. Abdullah Hashim",
    "Eng. Mohammed Heikel",
    "Eng. Hesham Abdelaziz",
    "Eng. Youssef Ossama",
    "Tech. Gomaa",
    "Tech. Ahmed Ali",
]

LINES = ["Line 3", "Line 7", "Line 9", "Line 10", "Line 12", "Line 13"]

PRIORITIES = ["Low", "Medium", "High", "CRITICAL"]

STATUSES = ["🔴 OPEN", "🟡 IN PROGRESS", "🟢 RESOLVED"]

@st.cache_resource
def get_google_sheet(site):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    creds_dict = json.loads(st.secrets["GOOGLE_SHEET_CREDENTIALS"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    
    spreadsheet = client.open_by_key("1urBkSsjlV2rO-uPbwbyKcjE_fl2lGnRD6tgNQEcXIMc")
    
    try:
        sheet = spreadsheet.worksheet(site)
    except:
        sheet = spreadsheet.add_worksheet(title=site, rows="1000", cols="20")
        headers = [
            'Submission_ID', 'Line_Number', 'Date_Submitted', 'Task', 
            'Spare_Parts_Data', 'Priority', 'Notes', 'Status', 
            'Submitted_By_Engineer', 'Expected_Due_Date', 'Troubleshooting_Steps',
            'Assigned_Engineer', 'Date_Resolved', 'Resolution_Notes'
        ]
        sheet.append_row(headers)
    
    return sheet

def load_data(site):
    sheet = get_google_sheet(site)
    try:
        all_values = sheet.get_all_values()
        
        if len(all_values) == 0:
            headers = [
                'Submission_ID', 'Line_Number', 'Date_Submitted', 'Task', 
                'Spare_Parts_Data', 'Priority', 'Notes', 'Status', 
                'Submitted_By_Engineer', 'Expected_Due_Date', 'Troubleshooting_Steps',
                'Assigned_Engineer', 'Date_Resolved', 'Resolution_Notes'
            ]
            sheet.append_row(headers)
            return pd.DataFrame(columns=headers)
        
        elif len(all_values) == 1:
            return pd.DataFrame(columns=all_values[0])
        
        else:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
            
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return pd.DataFrame(columns=[
            'Submission_ID', 'Line_Number', 'Date_Submitted', 'Task', 
            'Spare_Parts_Data', 'Priority', 'Notes', 'Status', 
            'Submitted_By_Engineer', 'Expected_Due_Date', 'Troubleshooting_Steps',
            'Assigned_Engineer', 'Date_Resolved', 'Resolution_Notes'
        ])

def save_problem(data, site):
    try:
        sheet = get_google_sheet(site)
        sheet.append_row(data)
        st.cache_resource.clear()
    except Exception as e:
        st.error(f"❌ Error saving problem: {str(e)}")
        raise e

def update_problem(row_index, updates, site):
    try:
        sheet = get_google_sheet(site)
        for col, value in updates.items():
            sheet.update_cell(row_index + 2, col, value)
        st.cache_resource.clear()
    except Exception as e:
        st.error(f"❌ Error updating problem: {str(e)}")
        raise e

def delete_problem(row_index, site):
    try:
        sheet = get_google_sheet(site)
        sheet.delete_rows(row_index + 2)
        st.cache_resource.clear()
    except Exception as e:
        st.error(f"❌ Error deleting problem: {str(e)}")
        raise e

def extract_unavailable_parts(df):
    """Extract all spare parts that are not in stock"""
    unavailable_parts = []
    
    for _, row in df.iterrows():
        if row['Spare_Parts_Data'] != "N/A" and row['Spare_Parts_Data'] != "":
            parts = row['Spare_Parts_Data'].split(" | ")
            for part in parts:
                try:
                    part_info = part.split(":")
                    if len(part_info) >= 4:
                        part_number = part_info[0]
                        part_name = part_info[1]
                        quantity = part_info[2]
                        stock_status = part_info[3]
                        
                        if "No" in stock_status:
                            unavailable_parts.append({
                                'Part_Number': part_number,
                                'Part_Name': part_name,
                                'Quantity': quantity
                            })
                except:
                    continue
    
    return pd.DataFrame(unavailable_parts)

if 'spare_parts' not in st.session_state:
    st.session_state.spare_parts = []
if 'troubleshooting_steps' not in st.session_state:
    st.session_state.troubleshooting_steps = []

st.sidebar.image("https://octa-solutions.com/storage/media/93fe1245-224d-459b-857e-5bf92ddd87ec.png?s=fb5d46c3ba508cd0a4a97f38ce1fa4c8", width=200)
st.sidebar.markdown("# 🏭 OCTA SERVICES SOLUTION")
st.sidebar.markdown("---")

selected_site = st.sidebar.selectbox("🏢 Select Site", SITES, key="site_selector")
st.sidebar.markdown(f"**Current Site:** {selected_site}")

st.sidebar.markdown("---")
if st.sidebar.button("🔄 REFRESH DATA"):
    st.cache_resource.clear()
    st.rerun()

page = st.sidebar.radio("Navigation", 
                        ["📊 Dashboard", 
                         "➕ Submit New Problem", 
                         "✅ Update Problem Status",
                         "✏️ Edit/Delete Entry",
                         "📜 History"])

st.sidebar.markdown("---")

if page == "📊 Dashboard":
    st.title(f"📊 DASHBOARD - {selected_site.upper()}")
    st.markdown("---")
    
    df = load_data(selected_site)
    
    if df.empty:
        st.warning("No problems recorded yet. Submit your first problem!")
    else:
        active_df = df[df['Status'].isin(['🔴 OPEN', '🟡 IN PROGRESS'])]
        
        if active_df.empty:
            st.success("🎉 All problems resolved! No active issues.")
        else:
            st.subheader("📈 SUMMARY BY LINE")
            cols = st.columns(len(LINES))
            
            for idx, line in enumerate(LINES):
                line_count = len(active_df[active_df['Line_Number'] == line])
                with cols[idx]:
                    st.metric(label=line, value=line_count)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_line = st.selectbox("Filter by Line", ["All"] + LINES)
            with col2:
                filter_priority = st.selectbox("Filter by Priority", ["All"] + PRIORITIES)
            with col3:
                filter_status = st.selectbox("Filter by Status", ["All", "🔴 OPEN", "🟡 IN PROGRESS"])
            
            filtered_df = active_df.copy()
            if filter_line != "All":
                filtered_df = filtered_df[filtered_df['Line_Number'] == filter_line]
            if filter_priority != "All":
                filtered_df = filtered_df[filtered_df['Priority'] == filter_priority]
            if filter_status != "All":
                filtered_df = filtered_df[filtered_df['Status'] == filter_status]
            
            st.markdown("---")
            
            # Check for overdue problems
            overdue_problems = []
            today = datetime.now().date()
            
            for idx, row in filtered_df.iterrows():
                try:
                    due_date = datetime.strptime(row['Expected_Due_Date'], "%d/%m/%Y").date()
                    if due_date < today:
                        days_overdue = (today - due_date).days
                        overdue_problems.append({
                            'ID': row['Submission_ID'],
                            'Line': row['Line_Number'],
                            'Task': row['Task'][:50] + "..." if len(row['Task']) > 50 else row['Task'],
                            'Days_Overdue': days_overdue,
                            'Priority': row['Priority'],
                            'Expected_Due': row['Expected_Due_Date']
                        })
                except:
                    continue
            
            # Show overdue warnings
            if overdue_problems:
                st.error(f"🚨 **URGENT: {len(overdue_problems)} OVERDUE PROBLEMS!**")
                overdue_df = pd.DataFrame(overdue_problems)
                overdue_df = overdue_df.sort_values('Days_Overdue', ascending=False)
                st.dataframe(overdue_df, use_container_width=True, hide_index=True)
                st.markdown("---")
            
            st.subheader(f"🔧 ACTIVE PROBLEMS ({len(filtered_df)})")
            
            if filtered_df.empty:
                st.info("No problems match your filters.")
            else:
                # Add Overdue Status column to filtered_df
                filtered_display = filtered_df.copy()
                filtered_display['Overdue_Status'] = ''
                
                for idx, row in filtered_display.iterrows():
                    try:
                        due_date = datetime.strptime(row['Expected_Due_Date'], "%d/%m/%Y").date()
                        if due_date < today:
                            days_overdue = (today - due_date).days
                            filtered_display.at[idx, 'Overdue_Status'] = f"⚠️ {days_overdue} days overdue"
                        elif due_date == today:
                            filtered_display.at[idx, 'Overdue_Status'] = "⏰ Due Today"
                        else:
                            days_remaining = (due_date - today).days
                            if days_remaining <= 2:
                                filtered_display.at[idx, 'Overdue_Status'] = f"🔔 Due in {days_remaining} days"
                            else:
                                filtered_display.at[idx, 'Overdue_Status'] = "✅ On Track"
                    except:
                        filtered_display.at[idx, 'Overdue_Status'] = "❓ Unknown"
                
                st.dataframe(filtered_display, use_container_width=True, hide_index=True)
                
                # Download active problems as CSV
                csv = filtered_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Active Problems (CSV)",
                    data=csv,
                    file_name=f"{selected_site}_active_problems_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            # Extract and display unavailable spare parts
            st.markdown("---")
            st.subheader("🔧 SPARE PARTS NOT AVAILABLE")
            
            unavailable_df = extract_unavailable_parts(filtered_df)
            
            if unavailable_df.empty:
                st.success("✅ All required spare parts are available!")
            else:
                st.warning(f"⚠️ {len(unavailable_df)} spare parts are not available")
                st.dataframe(unavailable_df, use_container_width=True, hide_index=True)
                
                # Download unavailable parts as CSV
                csv_unavailable = unavailable_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Unavailable Spare Parts (CSV)",
                    data=csv_unavailable,
                    file_name=f"{selected_site}_unavailable_parts_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

elif page == "➕ Submit New Problem":
    st.title(f"➕ SUBMIT NEW PROBLEM - {selected_site.upper()}")
    st.markdown("---")
    
    with st.form("new_problem_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            line_number = st.selectbox("Line Number *", LINES)
            date_submitted = st.date_input("Date Submitted *", value=datetime.now())
            expected_due_date = st.date_input("Expected Due Date *")
            submitted_by = st.selectbox("Your Name (Submitting Engineer) *", ENGINEERS)
            task = st.text_area("Task Description *", placeholder="Describe the problem...", height=150)
        
        with col2:
            priority = st.selectbox("Priority Level *", PRIORITIES)
            notes = st.text_area("Additional Notes", placeholder="Any extra information...", height=150)
        
        st.markdown("---")
        st.subheader("🔧 Spare Parts Required")
        st.markdown("Add spare parts needed for this task:")
        
        col_sp1, col_sp2, col_sp3, col_sp4 = st.columns([3, 3, 2, 2])
        with col_sp1:
            sp_number = st.text_input("Part Number", key="sp_num", placeholder="e.g., SP-12345")
        with col_sp2:
            sp_name = st.text_input("Part Name", key="sp_name", placeholder="e.g., Motor Bearing")
        with col_sp3:
            sp_stock = st.selectbox("In Stock?", ["Yes", "No"], key="sp_stock")
        with col_sp4:
            sp_qty = st.number_input("Quantity", min_value=1, value=1, key="sp_qty")
        
        add_spare_part = st.form_submit_button("➕ Add Spare Part")
        
        if add_spare_part and sp_number and sp_name:
            st.session_state.spare_parts.append({
                'number': sp_number,
                'name': sp_name,
                'stock': sp_stock,
                'quantity': sp_qty
            })
            st.success(f"✅ Added: {sp_name} ({sp_number})")
        
        if st.session_state.spare_parts:
            st.markdown("**Added Spare Parts:**")
            for idx, part in enumerate(st.session_state.spare_parts):
                st.text(f"{idx+1}. {part['name']} ({part['number']}) - Qty: {part['quantity']} - Stock: {part['stock']}")
        
        st.markdown("---")
        st.subheader("🔍 Troubleshooting Steps Already Taken")
        st.markdown("Document what you've already tried:")
        
        ts_step = st.text_input("Troubleshooting Step", key="ts_step", placeholder="e.g., Checked power supply - voltage normal")
        add_ts_step = st.form_submit_button("➕ Add Troubleshooting Step")
        
        if add_ts_step and ts_step:
            st.session_state.troubleshooting_steps.append(ts_step)
            st.success(f"✅ Added troubleshooting step")
        
        if st.session_state.troubleshooting_steps:
            st.markdown("**Troubleshooting Steps Taken:**")
            for idx, step in enumerate(st.session_state.troubleshooting_steps):
                st.text(f"{idx+1}. {step}")
        
        st.markdown("---")
        submitted = st.form_submit_button("🚀 SUBMIT PROBLEM", use_container_width=True)
        
        if submitted:
            if not line_number or not date_submitted or not task or not submitted_by or not expected_due_date:
                st.error("⚠️ Please fill in all required fields (*)")
            else:
                df = load_data(selected_site)
                submission_id = len(df) + 1 if not df.empty else 1
                
                date_submitted_str = date_submitted.strftime("%d/%m/%Y")
                expected_due_date_str = expected_due_date.strftime("%d/%m/%Y")
                
                spare_parts_str = " | ".join([
                    f"{p['number']}:{p['name']}:Qty{p['quantity']}:Stock-{p['stock']}" 
                    for p in st.session_state.spare_parts
                ]) if st.session_state.spare_parts else "N/A"
                
                ts_str = " | ".join(st.session_state.troubleshooting_steps) if st.session_state.troubleshooting_steps else "N/A"
                
                new_problem = [
                    submission_id,
                    line_number,
                    date_submitted_str,
                    task,
                    spare_parts_str,
                    priority,
                    notes if notes else "N/A",
                    "🔴 OPEN",
                    submitted_by,
                    expected_due_date_str,
                    ts_str,
                    "",
                    "",
                    ""
                ]
                
                save_problem(new_problem, selected_site)
                st.success(f"✅ Problem #{submission_id} submitted successfully!")
                show_floating_logos()
                
                st.session_state.spare_parts = []
                st.session_state.troubleshooting_steps = []

elif page == "✅ Update Problem Status":
    st.title(f"✅ UPDATE PROBLEM STATUS - {selected_site.upper()}")
    st.markdown("---")
    
    df = load_data(selected_site)
    
    if df.empty:
        st.warning("No problems recorded yet.")
    else:
        active_df = df[df['Status'] != '🟢 RESOLVED']
        
        if active_df.empty:
            st.success("🎉 All problems are resolved!")
        else:
            st.subheader("Select Problem to Update")
            
            problem_options = [f"ID #{row['Submission_ID']} - {row['Line_Number']} - {row['Task'][:50]}..." 
                             for _, row in active_df.iterrows()]
            
            selected_problem = st.selectbox("Choose Problem", problem_options)
            
            if selected_problem:
                problem_id = int(selected_problem.split("#")[1].split(" -")[0])
                problem_row = df[df['Submission_ID'] == problem_id].iloc[0]
                problem_index = df[df['Submission_ID'] == problem_id].index[0]
                
                st.markdown("---")
                st.subheader("📋 Problem Details")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Line:** {problem_row['Line_Number']}")
                    st.write(f"**Task:** {problem_row['Task']}")
                    st.write(f"**Priority:** {problem_row['Priority']}")
                    st.write(f"**Current Status:** {problem_row['Status']}")
                    st.write(f"**Submitted By:** {problem_row['Submitted_By_Engineer']}")
                
                with col2:
                    st.write(f"**Date Submitted:** {problem_row['Date_Submitted']}")
                    st.write(f"**Expected Due Date:** {problem_row['Expected_Due_Date']}")
                    st.write(f"**Notes:** {problem_row['Notes']}")
                
                if problem_row['Spare_Parts_Data'] != "N/A":
                    st.markdown("**Spare Parts:**")
                    parts = problem_row['Spare_Parts_Data'].split(" | ")
                    for part in parts:
                        st.text(f"  • {part.replace(':', ' - ')}")
                
                if problem_row['Troubleshooting_Steps'] != "N/A":
                    st.markdown("**Troubleshooting Steps Already Taken:**")
                    steps = problem_row['Troubleshooting_Steps'].split(" | ")
                    for idx, step in enumerate(steps):
                        st.text(f"  {idx+1}. {step}")
                
                st.markdown("---")
                st.subheader("🔄 Update Status")
                
                with st.form("update_form"):
                    new_status = st.selectbox("New Status", STATUSES)
                    assigned_engineer = st.selectbox("Assigned Engineer *", ENGINEERS,
                                                    index=ENGINEERS.index(problem_row['Assigned_Engineer']) if problem_row['Assigned_Engineer'] in ENGINEERS else 0)
                    
                    if new_status == "🟢 RESOLVED":
                        date_resolved = st.date_input("Date Resolved *", value=datetime.now())
                        resolution_notes = st.text_area("Resolution Notes *", placeholder="How was it fixed?")
                    else:
                        date_resolved = None
                        resolution_notes = ""
                    
                    update_button = st.form_submit_button("💾 UPDATE STATUS", use_container_width=True)
                    
                    if update_button:
                        if not assigned_engineer:
                            st.error("⚠️ Assigned engineer name is required!")
                        elif new_status == "🟢 RESOLVED" and (not date_resolved or not resolution_notes):
                            st.error("⚠️ Please fill in resolution date and notes for resolved problems!")
                        else:
                            date_resolved_str = date_resolved.strftime("%d/%m/%Y") if new_status == "🟢 RESOLVED" else ""
                            
                            updates = {
                                8: new_status,
                                12: assigned_engineer,
                                13: date_resolved_str,
                                14: resolution_notes if new_status == "🟢 RESOLVED" else ""
                            }
                            
                            update_problem(problem_index, updates, selected_site)
                            st.success(f"✅ Problem #{problem_id} updated successfully!")
                            show_floating_logos()
                            st.rerun()

elif page == "✏️ Edit/Delete Entry":
    st.title(f"✏️ EDIT/DELETE ENTRY - {selected_site.upper()}")
    st.markdown("---")
    
    df = load_data(selected_site)
    
    if df.empty:
        st.warning("No problems recorded yet.")
    else:
        st.subheader("Select Entry to Edit or Delete")
        
        # Show all entries (not just active ones)
        problem_options = [f"ID #{row['Submission_ID']} - {row['Line_Number']} - {row['Status']} - {row['Task'][:40]}..." 
                         for _, row in df.iterrows()]
        
        selected_problem = st.selectbox("Choose Entry", problem_options)
        
        if selected_problem:
            problem_id = int(selected_problem.split("#")[1].split(" -")[0])
            problem_row = df[df['Submission_ID'] == problem_id].iloc[0]
            problem_index = df[df['Submission_ID'] == problem_id].index[0]
            
            st.markdown("---")
            
            tab1, tab2 = st.tabs(["✏️ Edit Entry", "🗑️ Delete Entry"])
            
            with tab1:
                st.subheader("Edit Entry Details")
                
                with st.form("edit_form"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_line = st.selectbox("Line Number *", LINES, 
                                                index=LINES.index(problem_row['Line_Number']) if problem_row['Line_Number'] in LINES else 0)
                        
                        # Parse existing date
                        try:
                            existing_date_submitted = datetime.strptime(problem_row['Date_Submitted'], "%d/%m/%Y")
                        except:
                            existing_date_submitted = datetime.now()
                        edit_date_submitted = st.date_input("Date Submitted *", value=existing_date_submitted)
                        
                        try:
                            existing_due_date = datetime.strptime(problem_row['Expected_Due_Date'], "%d/%m/%Y")
                        except:
                            existing_due_date = datetime.now()
                        edit_expected_due = st.date_input("Expected Due Date *", value=existing_due_date)
                        
                        edit_submitted_by = st.selectbox("Submitted By *", ENGINEERS,
                                                        index=ENGINEERS.index(problem_row['Submitted_By_Engineer']) if problem_row['Submitted_By_Engineer'] in ENGINEERS else 0)
                        
                        edit_task = st.text_area("Task Description *", value=problem_row['Task'], height=150)
                    
                    with col2:
                        edit_priority = st.selectbox("Priority Level *", PRIORITIES,
                                                    index=PRIORITIES.index(problem_row['Priority']) if problem_row['Priority'] in PRIORITIES else 0)
                        
                        edit_status = st.selectbox("Status *", STATUSES,
                                                  index=STATUSES.index(problem_row['Status']) if problem_row['Status'] in STATUSES else 0)
                        
                        edit_notes = st.text_area("Additional Notes", 
                                                 value=problem_row['Notes'] if problem_row['Notes'] != "N/A" else "", 
                                                 height=150)
                        
                        edit_assigned = st.selectbox("Assigned Engineer", [""] + ENGINEERS,
                                                    index=ENGINEERS.index(problem_row['Assigned_Engineer']) + 1 if problem_row['Assigned_Engineer'] in ENGINEERS else 0)
                    
                    st.markdown("**Current Spare Parts:**")
                    if problem_row['Spare_Parts_Data'] != "N/A":
                        st.text(problem_row['Spare_Parts_Data'])
                    else:
                        st.text("No spare parts listed")
                    
                    st.markdown("**Current Troubleshooting Steps:**")
                    if problem_row['Troubleshooting_Steps'] != "N/A":
                        st.text(problem_row['Troubleshooting_Steps'])
                    else:
                        st.text("No troubleshooting steps listed")
                    
                    if edit_status == "🟢 RESOLVED":
                        st.markdown("---")
                        st.subheader("Resolution Information")
                        
                        try:
                            existing_resolved_date = datetime.strptime(problem_row['Date_Resolved'], "%d/%m/%Y") if problem_row['Date_Resolved'] else datetime.now()
                        except:
                            existing_resolved_date = datetime.now()
                        
                        edit_date_resolved = st.date_input("Date Resolved", value=existing_resolved_date)
                        edit_resolution_notes = st.text_area("Resolution Notes", 
                                                            value=problem_row['Resolution_Notes'] if problem_row['Resolution_Notes'] else "")
                    
                    st.markdown("---")
                    save_edit = st.form_submit_button("💾 SAVE CHANGES", use_container_width=True)
                    
                    if save_edit:
                        if not edit_line or not edit_task or not edit_submitted_by:
                            st.error("⚠️ Please fill in all required fields (*)")
                        else:
                            date_resolved_str = ""
                            resolution_notes_str = ""
                            
                            if edit_status == "🟢 RESOLVED":
                                date_resolved_str = edit_date_resolved.strftime("%d/%m/%Y")
                                resolution_notes_str = edit_resolution_notes
                            
                            updates = {
                                2: edit_line,
                                3: edit_date_submitted.strftime("%d/%m/%Y"),
                                4: edit_task,
                                6: edit_priority,
                                7: edit_notes if edit_notes else "N/A",
                                8: edit_status,
                                9: edit_submitted_by,
                                10: edit_expected_due.strftime("%d/%m/%Y"),
                                12: edit_assigned,
                                13: date_resolved_str,
                                14: resolution_notes_str
                            }
                            
                            update_problem(problem_index, updates, selected_site)
                            st.success(f"✅ Problem #{problem_id} updated successfully!")
                            show_floating_logos()
                            st.rerun()
            
            with tab2:
                st.subheader("⚠️ Delete Entry")
                st.warning("This action cannot be undone!")
                
                st.markdown("**Entry to Delete:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**ID:** {problem_row['Submission_ID']}")
                    st.write(f"**Line:** {problem_row['Line_Number']}")
                    st.write(f"**Task:** {problem_row['Task']}")
                    st.write(f"**Priority:** {problem_row['Priority']}")
                
                with col2:
                    st.write(f"**Status:** {problem_row['Status']}")
                    st.write(f"**Submitted By:** {problem_row['Submitted_By_Engineer']}")
                    st.write(f"**Date:** {problem_row['Date_Submitted']}")
                
                st.markdown("---")
                
                confirm_delete = st.checkbox("I confirm I want to delete this entry")
                
                if st.button("🗑️ DELETE ENTRY", type="primary", use_container_width=True, disabled=not confirm_delete):
                    delete_problem(problem_index, selected_site)
                    st.success(f"✅ Problem #{problem_id} deleted successfully!")
                    st.rerun()

elif page == "📜 History":
    st.title(f"📜 RESOLVED PROBLEMS HISTORY - {selected_site.upper()}")
    st.markdown("---")
    
    df = load_data(selected_site)
    
    if df.empty:
        st.warning("No problems recorded yet.")
    else:
        resolved_df = df[df['Status'] == '🟢 RESOLVED']
        
        if resolved_df.empty:
            st.info("No resolved problems yet.")
        else:
            st.subheader(f"📊 Total Resolved: {len(resolved_df)}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_line_hist = st.selectbox("Filter by Line", ["All"] + LINES, key="hist_line")
            with col2:
                unique_engineers = ["All"] + sorted([eng for eng in resolved_df['Assigned_Engineer'].unique() if eng])
                filter_engineer = st.selectbox("Filter by Assigned Engineer", unique_engineers)
            with col3:
                filter_priority_hist = st.selectbox("Filter by Priority", ["All"] + PRIORITIES, key="hist_priority")
            
            filtered_resolved = resolved_df.copy()
            if filter_line_hist != "All":
                filtered_resolved = filtered_resolved[filtered_resolved['Line_Number'] == filter_line_hist]
            if filter_engineer != "All":
                filtered_resolved = filtered_resolved[filtered_resolved['Assigned_Engineer'] == filter_engineer]
            if filter_priority_hist != "All":
                filtered_resolved = filtered_resolved[filtered_resolved['Priority'] == filter_priority_hist]
            
            st.markdown("---")
            
            if filtered_resolved.empty:
                st.info("No resolved problems match your filters.")
            else:
                # Download resolved problems as CSV
                csv_resolved = filtered_resolved.to_csv(index=False)
                st.download_button(
                    label="📥 Download Resolved Problems (CSV)",
                    data=csv_resolved,
                    file_name=f"{selected_site}_resolved_problems_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
                
                st.markdown("---")
                
                for idx, row in filtered_resolved.iterrows():
                    with st.expander(f"🆔 ID #{row['Submission_ID']} - {row['Line_Number']} - {row['Task'][:60]}... - Priority: {row['Priority']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Line:** {row['Line_Number']}")
                            st.markdown(f"**Task:** {row['Task']}")
                            st.markdown(f"**Priority:** {row['Priority']}")
                            st.markdown(f"**Submitted By:** {row['Submitted_By_Engineer']}")
                            st.markdown(f"**Date Submitted:** {row['Date_Submitted']}")
                            st.markdown(f"**Expected Due:** {row['Expected_Due_Date']}")
                        
                        with col2:
                            st.markdown(f"**Assigned Engineer:** {row['Assigned_Engineer']}")
                            st.markdown(f"**Date Resolved:** {row['Date_Resolved']}")
                            st.markdown(f"**Status:** {row['Status']}")
                            st.markdown(f"**Notes:** {row['Notes']}")
                        
                        st.markdown("---")
                        
                        if row['Spare_Parts_Data'] != "N/A":
                            st.markdown("**🔧 Spare Parts Used:**")
                            parts = row['Spare_Parts_Data'].split(" | ")
                            for part in parts:
                                st.text(f"  • {part.replace(':', ' - ')}")
                        
                        if row['Troubleshooting_Steps'] != "N/A":
                            st.markdown("**🔍 Troubleshooting Steps:**")
                            steps = row['Troubleshooting_Steps'].split(" | ")
                            for step_idx, step in enumerate(steps):
                                st.text(f"  {step_idx+1}. {step}")
                        
                        st.markdown(f"**✅ Resolution Notes:** {row['Resolution_Notes']}")
                
                st.markdown("---")
                st.subheader("📈 STATISTICS")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    total_resolved = len(filtered_resolved)
                    st.metric("Total Resolved", total_resolved)
                
                with col2:
                    critical_resolved = len(filtered_resolved[filtered_resolved['Priority'] == 'CRITICAL'])
                    st.metric("Critical Resolved", critical_resolved)
                
                with col3:
                    high_priority = len(filtered_resolved[filtered_resolved['Priority'] == 'High'])
                    st.metric("High Priority Resolved", high_priority)
