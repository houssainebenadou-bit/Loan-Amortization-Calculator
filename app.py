import streamlit as st
import pandas as pd
import plotly.express as px


def mensualite(capital, taux_annuel, duree_mois):
    t = taux_annuel / 12 / 100
    if t == 0:
        return capital / duree_mois
    return capital * t / (1 - (1 + t) ** -duree_mois)


def tableau_amortissement(capital, taux_annuel, duree_mois):
    t = taux_annuel / 12 / 100
    m = mensualite(capital, taux_annuel, duree_mois)
    reste = capital
    lignes = []
    for mois in range(1, duree_mois + 1):
        interets = reste * t
        capital_rembourse = m - interets
        reste -= capital_rembourse
        lignes.append({
            "Mois": mois,
            "Mensualité": round(m, 2),
            "Intérêts": round(interets, 2),
            "Capital remboursé": round(capital_rembourse, 2),
            "Reste dû": round(max(reste, 0), 2),
        })
    return pd.DataFrame(lignes)


st.title("Simulateur de crédit")

capital = st.number_input("Montant du crédit (DH)", min_value=1000, value=100000, step=1000)
taux = st.number_input("Taux annuel (%)", min_value=0.0, value=5.0, step=0.1)
duree = st.number_input("Durée (mois)", min_value=1, value=120, step=1)

if st.button("Calculer"):
    duree = int(duree)
    m = mensualite(capital, taux, duree)
    df = tableau_amortissement(capital, taux, duree)
    cout_total = m * duree - capital

    col1, col2 = st.columns(2)
    col1.metric("Mensualité", f"{m:,.2f} DH")
    col2.metric("Coût total du crédit", f"{cout_total:,.2f} DH")

    st.subheader("Tableau d'amortissement")
    st.dataframe(df, use_container_width=True)

    fig = px.line(df, x="Mois", y="Reste dû", title="Évolution du capital restant dû")
    st.plotly_chart(fig, use_container_width=True)


