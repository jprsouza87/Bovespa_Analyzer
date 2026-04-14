import streamlit as st
import plotly.graph_objects as go
from scraperfd import buscar_dados, buscar_por_nome, buscar_historico
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
st.caption("Análise baseada em VPA obrigatório, Endividamento, Dividend Yield e ROE")
st.divider()

# --- Inicializa session_state ---
if "ticker_selecionado" not in st.session_state:
    st.session_state.ticker_selecionado = ""
if "resultados_busca" not in st.session_state:
    st.session_state.resultados_busca = []
if "limpar_campos" not in st.session_state:
    st.session_state.limpar_campos = False

# --- Busca por nome ---
st.markdown("#### 🔍 Buscar empresa por nome")
col_busca, col_btn_busca, col_btn_limpar = st.columns([4, 1, 1])

with col_busca:
    termo = st.text_input("Nome", placeholder="ex: petrobras, itau, vale",
                          label_visibility="collapsed")
with col_btn_busca:
    buscar = st.button("Buscar", use_container_width=True)
with col_btn_limpar:
    if st.button("🗑️ Limpar", use_container_width=True):
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
    placeholder="ex: PETR4, ITUB4, WEGE3",
    label_visibility="collapsed"
)

ticker = ticker_direto if ticker_direto else st.session_state.ticker_selecionado

if st.button("Analisar", use_container_width=True) and ticker:
    with st.spinner(f"Buscando dados de {ticker.upper()}..."):
        try:
            dados = buscar_dados(ticker)
            r = analisar(dados)

            st.divider()

            # --- Métricas ---
            col1, col2, col3 = st.columns(3)
            col1.metric("Cotação Atual", f"R$ {dados['cotacao']:.2f}")
            col2.metric("VPA", f"R$ {dados['vpa']:.2f}")
            col3.metric("Patrimônio Líquido", f"R$ {dados['patrimonio_liq']/1e9:.1f} bi")

            st.divider()

            # --- Critérios (2x2 grid) ---
            col1, col2 = st.columns(2)

            with col1:
                icone = "✅" if r["vpa_ok"] else "❌"
                status = "Atendido" if r["vpa_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">VPA vs Cotação</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"Cotação R\\$ {dados['cotacao']:.2f} | VPA R\\$ {dados['vpa']:.2f}")

            with col2:
                icone = "✅" if r["endividamento_ok"] else "❌"
                status = "Atendido" if r["endividamento_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">Endividamento</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"{r['endividamento']:.2f}x patrimônio — limite 3,0x")

            col3, col4 = st.columns(2)

            with col3:
                icone = "✅" if r["dy_ok"] else "❌"
                status = "Atendido" if r["dy_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">Dividend Yield</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"{r['dividend_yield']*100:.1f}% — mínimo 6,0%")

            with col4:
                icone = "✅" if r["roe_ok"] else "❌"
                status = "Atendido" if r["roe_ok"] else "Não atendido"
                st.markdown(f"""
                    <div style="background:#1a1d27;border:1px solid #2a2d3a;border-radius:8px;padding:1rem;">
                        <div style="font-size:0.75rem;color:#888;margin-bottom:0.4rem;">ROE</div>
                        <div style="font-size:1.1rem;color:#e0e0e0;">{icone} {status}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.caption(f"{r['roe']*100:.1f}% — mínimo 15,0%")

            st.divider()

            # --- Recomendação ---
            if r["comprar"]:
                st.success(f"### {r['recomendacao']}", icon="✅")
            else:
                st.error(f"### {r['recomendacao']}", icon="❌")

            st.divider()

            # --- Gráfico ---
            st.markdown(f"#### 📈 Histórico de preços — {ticker.upper()} (últimos 12 meses)")
            hist = buscar_historico(ticker)

            if not hist.empty:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=hist.index,
                    y=hist["Close"],
                    mode="lines",
                    name="Fechamento",
                    line=dict(color="#4caf50", width=2),
                    fill="tozeroy",
                    fillcolor="rgba(76, 175, 80, 0.08)"
                ))
                fig.update_layout(
                    plot_bgcolor="#0f1117",
                    paper_bgcolor="#0f1117",
                    font=dict(color="#e0e0e0"),
                    xaxis=dict(
                        gridcolor="#2a2d3a",
                        showgrid=True,
                        rangeselector=dict(
                            bgcolor="#1a1d27",
                            activecolor="#4caf50",
                            bordercolor="#2a2d3a",
                            font=dict(color="#e0e0e0"),
                            buttons=list([
                                dict(count=1, label="1M", step="month", stepmode="backward"),
                                dict(count=3, label="3M", step="month", stepmode="backward"),
                                dict(count=6, label="6M", step="month", stepmode="backward"),
                                dict(count=12, label="12M", step="month", stepmode="backward"),
                            ])
                        ),
                        rangeslider=dict(
                            visible=True,
                            bgcolor="#1a1d27",
                            bordercolor="#2a2d3a",
                        ),
                        type="date"
                    ),
                    yaxis=dict(gridcolor="#2a2d3a", showgrid=True, tickprefix="R$ "),
                    margin=dict(l=10, r=10, t=10, b=10),
                    hovermode="x unified",
                    showlegend=False,
                    height=500,
                )
                st.plotly_chart(fig, use_container_width=True)

        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            import traceback
            st.error(str(e))
            st.code(traceback.format_exc())

st.markdown(
    "<div style='margin-top: 1.5rem; text-align: right; color: #666; font-size: 0.75rem;'>desenvolvido por João Paulo R. de Souza</div>",
    unsafe_allow_html=True
)
