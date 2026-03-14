import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

ADMIN_EMAIL = "abc@gmail.com"

st.title("💰 SpendWise")
st.subheader("Understand your spending habits with smart insights")

email = st.text_input("Enter your email")

if email:

    is_admin = email == ADMIN_EMAIL

    uploaded_file = st.file_uploader("Upload your expense CSV file", type=["csv"])

    if uploaded_file:

        try:
            df = pd.read_csv(uploaded_file)

            # clean column names
            df.columns = df.columns.str.strip()

            st.write("### Uploaded Expense Data")
            st.dataframe(df)

            # total spending
            total_spending = df["Amount"].sum()
            st.write("### Total Spending: ₹", total_spending)

            # category spending
            category_spending = df.groupby("Category")["Amount"].sum()

            st.write("### Spending by Category")

            fig, ax = plt.subplots()
            category_spending.plot(kind="pie", autopct="%1.1f%%", ax=ax)
            ax.set_ylabel("")
            st.pyplot(fig)

            st.write("### Category Breakdown")

            fig2, ax2 = plt.subplots()
            category_spending.plot(kind="bar", ax=ax2)
            ax2.set_xlabel("Category")
            ax2.set_ylabel("Amount")
            st.pyplot(fig2)

            # highest expense
            highest_expense = df.loc[df["Amount"].idxmax()]
            st.write("### Highest Expense")
            st.write(highest_expense)

            # biggest category
            top_category = category_spending.idxmax()
            st.write(f"### Highest Spending Category: {top_category}")

            # spending advice
            st.write("### 💡 SpendWise Advice")

            if total_spending > 5000:
                st.warning("You are spending quite a lot. Consider reducing expenses in food, shopping, or entertainment.")
            elif total_spending < 1000:
                st.info("Your spending is very low. You might allocate some money for personal growth or enjoyment.")
            else:
                st.success("Your spending looks balanced. Consider saving or investing some money.")

            # category advice
            if top_category == "Food":
                st.write("Tip: Cooking at home more often can help reduce food expenses.")
            elif top_category == "Shopping":
                st.write("Tip: Try limiting impulsive purchases and plan your shopping.")
            elif top_category == "Entertainment":
                st.write("Tip: Entertainment is great, but setting a monthly limit helps maintain balance.")

            # activity log for admin
            log = f"{datetime.now()} - {email} uploaded file with {len(df)} rows"

            if is_admin:
                st.sidebar.success("Admin Mode")
                st.sidebar.write("User activity log:")
                st.sidebar.write(log)

        except Exception as e:

            if is_admin:
                st.error("Admin Error Log")
                st.code(e)
            else:
                st.error("Something went wrong while processing the file.")