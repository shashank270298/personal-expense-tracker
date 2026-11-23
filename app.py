from datetime import date, datetime
from database import(
    init_db,
    add_expense,
    get_all_expenses,
    get_categories,
    get_monthly_summary,
    delete_expense,
    update_expense,
)
import pandas as pd
import streamlit as st

init_db()

st.set_page_config(page_title="Expense & Budget Tracker", layout="wide")

st.title("Personal Expense & Budget Tracker")

st.subheader("Add New Expense")
categories_dict = (
    get_categories()
)

with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3, col4 = st.columns(4)
    
    selected_cat = col1.selectbox("Category", list(categories_dict.keys()))
    amount = col2.number_input("Amount (₹)", min_value= 1.0, step=50.0)
    exp_date = col3.date_input("Date", value=date.today())
    note = col4.text_input("Note(Optional)")
    
    submitted = st.form_submit_button("Add Expense")
    
    if submitted:
        cat_id = categories_dict[selected_cat]["id"]
        add_expense(amount, cat_id, str(exp_date), note)
        st.success(f"Added ₹{amount:.2f} under {selected_cat}.")
        st.rerun()


st.subheader("Monthly Budget Status")
current_month = date.today().strftime( "%Y-%m")
summary_rows = get_monthly_summary(current_month)

summary_data = []

for cat_name, limit_amt, spent_amt in summary_rows:
    remaining = limit_amt - spent_amt
    status = "Over Budget" if spent_amt > limit_amt else "Within Budget"
    summary_data.append({
        "Category": cat_name,
        "Monthly Limit (₹)": round(limit_amt,2),
        "Total Spent (₹)": round(spent_amt, 2),
        "Remaining (₹)": round(remaining, 2),
    })
    
st.dataframe(pd.DataFrame(summary_data), use_container_width=True)

st.subheader("Expense History")

rows = get_all_expenses()

if rows:
    df = pd.DataFrame(
        rows, columns = ["ID", "Date", "Category", "Amount (₹)", "Note"]
    )
    st.dataframe(df, use_container_width=True)
    
    csv_file = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download CSV File",
        data=csv_file,
        file_name=f"expense_{current_month}.csv",
        mime="text/csv",
    )
    
    st.divider()
    st.subheader("Edit or Delete an Existing Expense")
    
    expenses_by_id = {row[0]: row for row in rows}
    selected_id = st.selectbox(
        "Select Expense ID",
        options=list(expenses_by_id.keys()),
        format_func=lambda eid:(
            f"ID {eid} | {expenses_by_id[eid][1]} | {expenses_by_id[eid][2]} |"
            f" ₹{expenses_by_id[eid][3]:.2f}"
        ),
    )
    
    _, existing_date_str, existing_cat, existing_amt, existing_note = (
        expenses_by_id[selected_id]     
    )
    cat_names = list(categories_dict.keys())
    default_cat_index = (
        cat_names.index(existing_cat) if existing_cat in cat_names else 0
    )
    default_date = datetime.strptime(existing_date_str, "%Y-%m-%d").date()
    
    with st.form("edit_expense_form"):
        ecol1, ecol2, ecol3, ecol4 = st.columns(4)
        edit_cat = ecol1.selectbox(
            "Category", options=cat_names, index=default_cat_index
        )
        edit_amount = ecol2.number_input(
            "Amount (₹)", min_value=1.0, value=float(existing_amt), step=50.0
        )
        edit_date = ecol3.date_input("Date", value=default_date)
        edit_note = ecol4.text_input("Note", value=existing_note or "")
        
        bcol1, bcol2 = st.columns(2)
        update_clicked = bcol1.form_submit_button("Update Expense")
        delete_clicked = bcol2.form_submit_button("Delete Expense")
        
        if update_clicked:
            new_cat_id = categories_dict[edit_cat]["id"]
            update_expense(
                selected_id, edit_amount, new_cat_id, str(edit_date), edit_note
            )
            st.success(f"Updated Expense ID {selected_id}.")
            st.rerun()
            
        if delete_clicked:
            delete_expense(selected_id)
            st.warning(f"Deleted Expense ID {selected_id}.")
            st.rerun()    
else:
    st.info("No expense record exist.")