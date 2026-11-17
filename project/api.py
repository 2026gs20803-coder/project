import requests

API_URL = 'https://career.go.kr'

def search_external_uns(keyword):
    if keyword.strip() == '':
        return []
    params = {
    'q':keyword,
    'limit':5
    }

    try:
        response = requests.get(API_URL, params=params, timeout=5)
        data = response.json()

    except requests.RequestException:
        print('네트워크 오류가 발생했습니다.')
    except ValueError:
        print('응답 데이터를 처리할 수 없습니다.')
        return []
    
    results = []
    
    for item in data.get('docs', []):
        region = item.get('region', '지역 없음')
        un_list = item.get('un_name', [])
        address = item.get('address', '주소 없음')
        Ft = item.get('Ft', '설립 유형 없음')
        if len(un_list) > 0:
            un = un_list[0]
        else:
            un = '대학교 정보 없음'

        university = {
            'region':region,
            'un':un,
            'address':address,
            'Ft': Ft
        }
        results.append(university)
    return results