import streamlit as st
from collections import defaultdict, deque

def main():
    st.title("スタジョ野球守備ポジション")
    st.title("Stable Matching")
    st.header("⚾ 選手の希望入力")
    st.markdown("**選手名｜第一希望｜第二希望（横並び）**")

    default_players = [
        ("しょうま", "2", "1"),
        ("たかゆき", "1", "2"),
        ("あきと", "1", "6"),
        ("ゆうと", "2", "3"),
        ("たくみ", "2", "1"),
        ("ひなた", "2", "4"),
        ("ようすけ", "1", "4"),
        ("ゆうま", "5", "6"),
        ("こうせい", "2", "1"),
        ("りょう", "5", "6"),
        ("そうた", "1", "8"),
        ("たいち", "1", "5"),
        ("ひろあ", "2", "1"),
        ("りんな", "1", "2"),
    ]

    player_prefs = {}
    player_count = st.number_input("選手数", min_value=1, max_value=20, value=len(default_players), step=1)

    for i in range(player_count):
        col1, col2, col3 = st.columns(3)
        name_default, first_default, second_default = default_players[i] if i < len(default_players) else (f"選手{i+1}", "", "")
        with col1:
            name = st.text_input("選手名", value=name_default, key=f"name_{i}")
        with col2:
            first = st.text_input("第一希望", value=first_default, key=f"pref1_{i}")
        with col3:
            second = st.text_input("第二希望", value=second_default, key=f"pref2_{i}")
        if name:
            player_prefs[name] = [first, second]

    st.header("🏆 監督の希望入力")
    st.markdown("**選手名｜第一希望｜第二希望（横並び）**")
    position_prefs_raw = defaultdict(list)
    for i in range(player_count):
        col1, col2, col3 = st.columns(3)
        name_default = default_players[i][0] if i < len(default_players) else f"選手{i+1}"
        with col1:
            name = st.text_input("選手名", value=name_default, key=f"coach_name_{i}")
        with col2:
            coach1 = st.text_input("第一希望", key=f"coach_pref1_{i}")
        with col3:
            coach2 = st.text_input("第二希望", key=f"coach_pref2_{i}")
        for pos in [coach1, coach2]:
            if name and pos:
                position_prefs_raw[pos].append(name)

    if st.button("マッチング開始"):
        # 全選手の希望に控えを加える
        full_prefs = {
            player: [p for p in prefs + ["控え"] if p]
            for player, prefs in player_prefs.items()
        }

        matches = stable_matching(full_prefs, position_prefs_raw)
        st.subheader("📋 マッチング結果")
        for pos, players in sorted(matches.items()):
            st.write(f"ポジション {pos}: {', '.join(players)}")

def stable_matching(player_preferences, position_preferences):
    free_positions = deque(position_preferences.keys())  # 監督優先でアプローチ
    proposals = defaultdict(set)
    matches = {}
    capacity = {str(i): 1 for i in range(1, 10)}
    capacity["控え"] = 3

    player_rank = {
        player: {pos: rank for rank, pos in enumerate(prefs)}
        for player, prefs in player_preferences.items()
    }

    while free_positions:
        position = free_positions.popleft()
        prefs = position_preferences[position]
        for player in prefs:
            if player in proposals[position]:
                continue
            proposals[position].add(player)

            if position not in matches:
                matches[position] = [player]
            else:
                matches[position].append(player)

            if len(matches[position]) > capacity.get(position, 1):
                ranked = sorted(
                    matches[position],
                    key=lambda x: player_rank.get(x, {}).get(position, float('inf'))
                )
                matches[position] = ranked[:capacity[position]]
                for r in ranked[capacity[position]:]:
                    pass  # 再アプローチなし（監督優先）
            break

        if len(matches.get(position, [])) < capacity.get(position, 1):
            free_positions.append(position)

    return {pos: sorted(players) for pos, players in matches.items()}

if __name__ == "__main__":
    main()
