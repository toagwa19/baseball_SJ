import streamlit as st
import google.generativeai as genai
from collections import defaultdict
import random


# --- API キーの設定 ---
API_KEY = "AIzaSyD3sy0YJ_eyu4DO-iDGMd50wR_nYSoKL7s"  # ← ここに取得した API キーを入力
genai.configure(api_key=API_KEY)

def main():
    st.set_page_config(layout="wide")  # ページ幅を広く設定
    st.title("SJポジション")

    st.header("📝選手情報の入力")
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

    st.markdown("#### 選手名｜第一希望｜第二希望｜監督希望")
    for name, first, second in player_data:
        cols = st.columns([2, 1, 1, 1])
        with cols[0]:
            name_input = st.text_input("選手名", value=name, key=f"name_{name}", label_visibility="collapsed")
        with cols[1]:
            first_input = st.text_input("第一希望", value=str(first), key=f"first_{name}", label_visibility="collapsed")
        with cols[2]:
            second_input = st.text_input("第二希望", value=str(second), key=f"second_{name}", label_visibility="collapsed")
        with cols[3]:
            coach_input = st.text_input("監督希望", key=f"coach_{name}", label_visibility="collapsed")

        name_input = name_input.strip()
        first_input = first_input.strip()
        second_input = second_input.strip()

        # 🔽 マッチング対象チェック（選手名と第一希望が必須）
        if name_input and first_input:
            player_prefs[name_input] = [first_input, second_input]

            if coach_input.strip():
                pos = coach_input.strip()
                coach_ranks[pos][name_input] = 0  # 評価がある選手はランク0

    user_input ="この鷺宮スタージョーズの守備ポジションについて、どう思いますか？" 
    if st.button("▶️ マッチング開始"):
        matches = stable_matching_player_priority(player_prefs, coach_ranks)
        st.subheader("📄 マッチング結果")
        for pos in sorted(matches.keys()):
            user_input = user_input + f" ポジション {pos}: {', '.join(matches[pos])}" 
            st.write(f"ポジション {pos}: {', '.join(matches[pos])}")
        # ✅ AIモデル指定
        st.subheader("🤖 スタジョAI の応答:")
        model = genai.GenerativeModel("gemini-2.5-pro-exp-03-25")  
        # ✅ generate_content() の修正
        response = model.generate_content([user_input])
        # ✅ レスポンスの取得方法を修正

        st.write(response.text if hasattr(response, 'text') else "応答が取得できませんでした。")  

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
