import streamlit as st
from scraper import buscar_dados, buscar_por_nome
from analyzer import analisar

st.set_page_config(
    page_title="Analisador B3",
    page_icon="📊",
    layout="centered"
)

st.markdown("""
    <style>
        .stApp { background-color: #0f1117; color: #e0e0e0; }
        h1, h2, h3 { color: #e0e0e0; font-family: Georgia, serif; }
        div[data-testid="metric-container"] { background-color: #1a1d27; border: 1px solid #2a2d3a; border-radius: 8px; padding: 1rem; }
        div[data-testid="stButton"] button { background-color: #1a1d27; color: #e0e0e0; border: 1px solid #2a2d3a; width: 100%; }
        div[data-testid="stButton"] button:hover { border-color: #4caf50; color: #4caf50; }
    </style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Analisador Fundamentalista — B3")
st.caption("Análise baseada em Valor Patrimonial, Endividamento e Dividend Yield")
st.divider()

# --- Inicializa session_state ---
if "ticker_selecionado" not in st.session_state:
    st.session_state.ticker_selecionado = ""
if "resultados_busca" not in st.session_state:
    st.session_state.resultados_busca = []

# --- Busca por nome ---
st.markdown("#### 🔍 Buscar empresa por nome")
col_busca, col_btn_busca, col_btn_limpar = st.columns([4, 1, 1])
with col_busca:
    termo = st.text_input("Nome", placeholder="ex: petrobras, itau, vale",
                          label_visibility="collapsed", key="busca_nome")
with col_btn_busca:
    buscar = st.button("Buscar", use_container_width=True)
with col_btn_limpar:
    limpar = st.button("🗑️ Limpar", use_container_width=True)

if limpar:
    st.session_state.ticker_selecionado = ""
    st.session_state.resultados_busca = []
    st.rerun()

if buscar and termo:
    with st.spinner("Buscando empresas..."):
        try:
            st.session_state.resultados_busca = buscar_por_nome(termo)
            st.session_state.ticker_selecionado = ""
        except Exception as e:
            st.error(str(e))

if st.session_state.resultados_busca:
    opcoes = {f"{r['papel']} — {r['nome']}": r["papel"] for r in st.session_state.resultados_busca}
    escolha = st.selectbox("Selecione o papel:", list(opcoes.keys()))
    if escolha:
        st.session_state.ticker_selecionado = opcoes[escolha]

st.divider()

# --- Input direto por código ---
st.markdown("#### 📊 Ou digite o código diretamente")
ticker_direto = st.text_input(
    "Código",
    value=st.session_state.ticker_selecionado,
    placeholder="ex: PETR4, ITUB4, WEGE3",
    label_visibility="collapsed",
    key="input_ticker"
)

ticker = ticker_direto if ticker_direto else st.session_state.ticker_selecionado

if st.button("Analisar", use_container_width=True) and ticker:
    with st.spinner(f"Buscando dados de {ticker.upper()}..."):
        try:
            dados = buscar_dados(ticker)
            r = analisar(dados)

            st.divider()

            col1, col2, col3 = st.columns(3)
            col1.metric("Cotação Atual", f"R$ {dados['cotacao']:.2f}")
            col2.metric("VPA", f"R$ {r['vpa']:.2f}")
            col3.metric("Patrimônio Líquido", f"R$ {dados['patrimonio_liq']/1e9:.1f} bi")

            st.divider()

            col4, col5, col6 = st.columns(3)

            with col4:
                icone = "✅" if r["vpa_ok"] else "❌"
                status = "Atendido" if r["vpa_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">VPA vs Cotação</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"Cotação R\\$ {dados['cotacao']:.2f} | VPA R\\$ {r['vpa']:.2f}")

            with col5:
                icone = "✅" if r["endividamento_ok"] else "❌"
                status = "Atendido" if r["endividamento_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">Endividamento</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"{r['endividamento']:.2f}x patrimônio — limite 3,0x")

            with col6:
                icone = "✅" if r["dy_ok"] else "❌"
                status = "Atendido" if r["dy_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">Dividend Yield</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"{r['dividend_yield']*100:.1f}% — mínimo 6,0%")

            st.divider()

            if r["comprar"]:
                st.success(f"### {r['recomendacao']}", icon="✅")
            else:
                st.error(f"### {r['recomendacao']}", icon="❌")

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            import traceback
            st.error(str(e))
            st.code(traceback.format_exc())