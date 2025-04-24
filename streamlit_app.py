import streamlit as st
from collections import defaultdict
import random

# カスタムCSSでスマホ対応の4項目横並び入力
st.markdown("""
<style>
    .input-row {
        display: flex;
        flex-wrap: nowrap;
        gap: 4px;
        margin-bottom: 8px;
    }
    .input-row > div {
        flex: 1;
    }
    .stTextInput > div > input {
        font-size: 14px;
        padding: 4px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("⚾ 野球守備ポジション 安定マッチング")
    st.markdown("スマホ画面でも見やすいように調整済み")

    # 初期データ
    player_data = [
        ("しょうま", 2, 1),
        ("たかゆき", 1, 2),
        ("あきと", 1, 6),
        ("ゆうと", 2, 3),
        ("たくみ", 2, 1),
        ("ひなた", 2, 4),
        ("ようすけ", 1, 4),
        ("ゆうま", 5, 6),
        ("こうせい", 2, 1),
        ("りょう", 5, 6),
        ("そうた", 1, 8),
        ("たいち", 1, 5),
        ("ひろあ", 2, 1),
        ("りんな", 1, 2)
    ]

    st.markdown("#### 選手名｜第一希望｜第二希望｜監督の評価ポジション")

    player_prefs = {}
    coach_ranks = defaultdict(dict)

    for name, first, second in player_data:
        st.markdown('<div class="input-row">', unsafe_allow_html=True)
        col1 = st.text_input("", value=name, key=f"name_{name}", label_visibility="collapsed", placeholder="選手名")
        col2 = st.text_input("", value=str(first), key=f"first_{name}", label_visibility="collapsed", placeholder="第一希望")
        col3 = st.text_input("", value=str(second), key=f"second_{name}", label_visibility="collapsed", placeholder="第二希望")
        col4 = st.text_input("", key=f"coach_{name}", label_visibility="collapsed", placeholder="監督の評価")
        st.markdown('</div>', unsafe_allow_html=True)

        if col1.strip():
            player_prefs[col1.strip()] = [col2.strip(), col3.strip()]
            if col4.strip():
                coach_ranks[col4.strip()][col1.strip()] = 0

    if st.button("🎲 マッチング開始"):
        matches = stable_matching_player_priority(player_prefs, coach_ranks)
        st.subheader("📄 マッチング結果")
        for pos in sorted(matches.keys()):
            st.write(f"ポジション {pos}: {', '.join(matches[pos])}")

def stable_matching_player_priority(player_prefs, coach_ranks):
    matches = {str(i): [] for i in range(1, 10)}
    capacity = {str(i): 1 for i in range(1, 10)}
    unassigned_players = list(player_prefs.keys())
    random.shuffle(unassigned_players)

    for player in unassigned_players:
        prefs = player_prefs[player]
        assigned = False

        for pos in prefs:
            if len(matches[pos]) < capacity[pos]:
                matches[pos].append(player)
                assigned = True
                break
            else:
                current_player = matches[pos][0]
                rank_current = coach_ranks.get(pos, {}).get(current_player, float('inf'))
                rank_new = coach_ranks.get(pos, {}).get(player, float('inf'))

                if rank_new < rank_current:
                    matches[pos][0] = player
                    unassigned_players.append(current_player)
                    assigned = True
                    break
                elif rank_new == rank_current:
                    if random.choice([True, False]):
                        matches[pos][0] = player
                        unassigned_players.append(current_player)
                        assigned = True
                        break

        if not assigned:
            for pos in matches:
                if len(matches[pos]) < capacity[pos]:
                    matches[pos].append(player)
                    break

    return {pos: sorted(players) for pos, players in matches.items()}

if __name__ == "__main__":
    main()
