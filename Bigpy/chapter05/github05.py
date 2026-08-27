import requests
import csv

def get_github_top_repos():
    url = "https://api.github.com/search/repositories"
    params = {
        "q":"language:python", 
        "sort":"stars", 
        "order":"desc", 
        "per_page":10
    }

    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()

    # print(data)

    items = data['items']
    print("===== python 인기 저장소 TOP10 =====")

    results = []

    for idx, item in enumerate(items, start=1):
        name = item['full_name']
        stars = item['stargazers_count']
        html_url = item['html_url']

        print(f"{idx}위 | {name} | ⭐ {stars:,} | {html_url}")

        results.append({
            "순위": idx, 
            "이름": name, 
            "star수": stars, 
            "URL":html_url
        })

    print()
    print("=== star 10,000개 이상 저장소 ===")

    high_star_repos = [r for r in results if r["star수"] >= 10000]
    for r in high_star_repos:
        print(f"{r['이름']} ({r['star수']:,})")

    # csv 저장 (csv 저장할때 newline="" 은 필수로 하는게 좋음)
    # 이미 갖고 있는 딕셔너리를 CSV의 한 줄(값들의 나열)로 바꿔주는 역할
    csv_path = "github_top10.csv"
    with open(csv_path, "w", newline="", encoding='utf-8-sig') as f:      #
        writer = csv.DictWriter(f, fieldnames=["순위", "이름", "star수", "URL"])
        writer.writeheader()    # 컬럼 이름을 fieldnames로 씀
        writer.writerows(results)    # 저장

    print()
    print("저장완료")

if __name__ == "__main__":
    get_github_top_repos()

