import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="ERP System", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None
    st.session_state.role = None



def api_sell(token, product, quantity, price):
    return requests.post(
        f"{API_URL}/sell",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "product": product,
            "quantity": quantity,
            "total": quantity * price
        }
    )


def api_sales(token):
    return requests.get(
        f"{API_URL}/sales",
        headers={"Authorization": f"Bearer {token}"}
    )


if not st.session_state.token:
    st.title("ERP Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(
            f"{API_URL}/login",
            json={"username": username, "password": password}
        )

        if res.status_code == 200:
            data = res.json()
            st.session_state.token = data["access_token"]
            st.session_state.role = data["role"]
            st.rerun()
        else:
            st.error("Invalid login")


else:
    st.sidebar.title("Menu")
    st.sidebar.write(f"Role: **{st.session_state.role}**")

    if st.sidebar.button("Logout"):
        st.session_state.token = None
        st.session_state.role = None
        st.rerun()

    st.title("ERP Dashboard")

    
    if st.sidebar.button("Inventory"):
        res = requests.get(
            f"{API_URL}/inventory",
            headers={"Authorization": f"Bearer {st.session_state.token}"}
        )

        if res.status_code == 200:
            st.subheader("📦 Inventory")
            st.dataframe(res.json())
        else:
            st.error("Access denied")

    
    st.divider()
    st.subheader(" Sales")
    if st.session_state.role in ["admin", "staff"]:
        product = st.text_input("Product name")
        qty = st.number_input("Quantity", min_value=1, step=1)
        price = st.number_input("Price", min_value=1.0, step=1.0)

        if st.button("Confirm Sale"):
            res = api_sell(
                st.session_state.token,
                product,
                qty,
                price
            )

            if res.status_code == 200:
                st.success(" Sale recorded successfully")
            else:
                st.error(" Sale failed")

    else:
        st.warning("Sales access denied")

    # ---------- SALES REPORT (ADMIN ONLY) ----------
    if st.session_state.role == "admin":
        st.divider()
        st.subheader(" Sales Report")

        res = api_sales(st.session_state.token)
        if res.status_code == 200:
            st.dataframe(res.json())
        else:
            st.error("Unable to load sales data")

    
    st.divider()
    st.subheader(" AI Assistant")

    question = st.text_input("Ask about stock or offers")
    if st.button("Ask AI") and question:
        res = requests.post(
            f"{API_URL}/chat",
            json={"question": question}
        )
        st.success(res.json()["answer"])
