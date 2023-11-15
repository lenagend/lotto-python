import schedule
import time
from src.db_setup import conn
from src.collect_lotto_data import get_lotto_data, save_lotto_data


def fetch_latest_draw_no_from_db():
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(drawNo) FROM LottoDraws")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None


def fetch_and_save_next_draw_data():
    latest_draw_no = fetch_latest_draw_no_from_db()
    if latest_draw_no is not None:
        next_draw_no = latest_draw_no + 1
        lotto_data = get_lotto_data(next_draw_no)
        if lotto_data:
            save_lotto_data(lotto_data)
            print(f"{next_draw_no} 회차 데이터를 가져와서 저장했습니다.")


# 매주 일요일 자정에 fetch_and_save_draw_data 함수 실행 스케줄링
schedule.every().sunday.at("00:00").do(fetch_and_save_next_draw_data)

while True:
    schedule.run_pending()
    time.sleep(1)
