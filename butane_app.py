import streamlit as st
import math

def main():
    st.title("Butane Inventory Calculator")

    # Input fields
    col1, col2 = st.columns(2)
    with col1:
        refill_price = st.number_input("Refill Price:", min_value=0.0, value=0.0)
        brand_new_price = st.number_input("Brand New Price:", min_value=0.0, value=0.0)
        out = st.number_input("Out (Stocks taken out):", min_value=0, value=0)
    with col2:
        bo = st.number_input("B.O. (Back out/unsellable):", min_value=0, value=0)
        remain = st.number_input("Remain (Remaining items):", min_value=0, value=0)
        empty_cans = st.number_input("Empty Cans (Exchanged):", min_value=0, value=0)

    # --- Calculation Confirmation Flow ---
    if st.button("Calculate"):
        st.session_state.show_calc_confirm = True

    if st.session_state.get("show_calc_confirm", False):
        st.warning("Are you sure you want to calculate?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes - Calculate"):
                try:
                    total_sold = out - bo - remain
                    refills_sold = empty_cans
                    brand_new_sold = total_sold - empty_cans
                    refill_money = refills_sold * refill_price
                    brand_new_money = brand_new_sold * brand_new_price
                    total_money = refill_money + brand_new_money

                    # Save to session state to persist results
                    st.session_state.calc_result = {
                        "total_sold": total_sold,
                        "refills_sold": refills_sold,
                        "brand_new_sold": brand_new_sold,
                        "refill_money": refill_money,
                        "brand_new_money": brand_new_money,
                        "total_money": total_money
                    }

                    st.success("Calculation completed successfully!")
                except ValueError:
                    st.error("Please enter valid numbers in all fields")

                st.session_state.show_calc_confirm = False

        with col2:
            if st.button("No - Cancel"):
                st.session_state.show_calc_confirm = False

    # --- Display Calculation Results if available ---
    if "calc_result" in st.session_state:
        result = st.session_state.calc_result
        st.subheader("Calculation Results")
        st.write(f"Total sold: {result['total_sold']}")
        st.write(f"Refills sold: {result['refills_sold']}")
        st.write(f"Brand New Butane sold: {result['brand_new_sold']}")
        st.write(f"Refill Money to Remit: {result['refill_money']:.2f}")
        st.write(f"Brand New Money to Remit: {result['brand_new_money']:.2f}")
        st.write(f"Total Money to Remit: {result['total_money']:.2f}")

    st.markdown("---")
    st.subheader("Add Expenses")
    expense_name = st.text_input("Expense Name:")
    expense_amount = st.number_input("Amount:", min_value=0.0, value=0.0)

    if 'expenses' not in st.session_state:
        st.session_state.expenses = []

    if st.button("Add Expense"):
        if not expense_name:
            st.error("Please enter an expense name")
        else:
            st.session_state.show_expense_confirm = True

    if st.session_state.get("show_expense_confirm", False):
        st.warning(f"Are you sure you want to add the expense: {expense_name} - {expense_amount:.2f}?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes - Add Expense"):
                st.session_state.expenses.append((expense_name, expense_amount))
                st.success(f"Added expense: {expense_name} - {expense_amount:.2f}")
                st.session_state.show_expense_confirm = False
        with col2:
            if st.button("No - Cancel"):
                st.session_state.show_expense_confirm = False

    # --- Display Expense List ---
    if st.session_state.expenses:
        st.subheader("Expenses List")
        for name, amount in st.session_state.expenses:
            st.write(f"{name}: {amount:.2f}")

    st.markdown("---")
    if st.button("Final Calculation"):
        if 'calc_result' not in st.session_state:
            st.error("Please calculate inventory first")
        else:
            st.session_state.show_final_confirm = True

    if st.session_state.get("show_final_confirm", False):
        st.warning("Are you sure you want to perform the final calculation?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes - Final Calculate"):
                total_money = st.session_state.calc_result['total_money']
                total_expenses = sum(amount for (_, amount) in st.session_state.expenses)
                final_money = total_money - total_expenses

                st.session_state.final_result = {
                    "total_money": total_money,
                    "total_expenses": total_expenses,
                    "final_money": final_money
                }
                st.success("Final calculation completed!")
                st.session_state.show_final_confirm = False
        with col2:
            if st.button("No - Cancel"):
                st.session_state.show_final_confirm = False

    # --- Display Final Calculation if available ---
    if "final_result" in st.session_state:
        final = st.session_state.final_result
        st.subheader("Final Calculation")
        st.write(f"Total Money to Remit: {final['total_money']:.2f}")
        st.write(f"Total Expenses: {final['total_expenses']:.2f}")
        st.write(f"Final Money to Remit: {final['final_money']:.2f}")

if __name__ == "__main__":
    main()
