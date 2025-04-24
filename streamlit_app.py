import streamlit as st
from collections import defaultdict
import random

def main():
    st.title("野球守備ポジション 安定マッチング（選手優先＋監督評価）")

    st.header("📝 選手情報の入力")
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

    player_prefs = {}
    coach_ranks = defaultdict(dict)

    st.markdown("#### 選手名　｜　第一希望　｜　第二希望　｜　監督の希望")
    for name, first, second in player_data:
        col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1, 0.1])  # スマホ対応レイアウト
        with col1:
            name_input = st.text_input("選手名", value=name, key=f"name_{name}", label_visibility="collapsed")
        with col2:
            first_input = st.text_input("第一希望", value=str(first), key=f"first_{name}", label_visibility="collapsed")
        with col3:
            second_input = st.text_input("第二希望", value=str(second), key=f"second_{name}", label_visibility="collapsed")
        with col4:
            coach_input = st.text_input("監督の評価ポジション", key=f"coach_{name}", label_visibility="collapsed")

        name_input = name_input.strip()
        prefs = [first_input.strip(), second_input.strip()]
        player_prefs[name_input] = prefs

        if coach_input.strip():
            pos = coach_input.strip()
            coach_ranks[pos][name_input] = 0  # 高評価をランク0に設定

    if st.button("▶️ マッチング開始"):
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
            # ランダムで空いているポジションに割当て
            for pos in matches:
                if len(matches[pos]) < capacity[pos]:
                    matches[pos].append(player)
                    break

    return {pos: sorted(players) for pos, players in matches.items()}

if __name__ == "__main__":
    main()
