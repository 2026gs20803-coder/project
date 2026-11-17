import streamlit as st
from database import (create_table, 
                      add_university, 
                      get_all_uns, 
                      update_rating,  
                      delete_university,
                      search_uns)

from api import search_external_uns

create_table()

def print_uns(rows):
  if len(rows) == 0:
    st.info('등록된 대학교가 없습니다.')
    return

  st.write(f'총 {len(rows)} 곳')
  st.write('---')
#   st.dataframe(rows)

  for row in rows:
    id = row[0]
    region = row[1]
    un = row[2]
    rating = row[3]
    address = row[4]
    Ft = row[5]
    
    if rating == 0: rating_text = '평점 없음'
    else: rating_text = f"{rating}점"

    st.write(f'{id}./{un} / {address}/ {region} / {Ft} / {rating_text}')

    col1, col2 = st.columns([1, 1])


    with col1: # 평점
       current_rate = rating if 1<=rating<=5 else 1
       new_rating = st.selectbox('평점', options=[1,2,3,4,5],
                                 index=current_rate-1,
                                 key=f'rate_sel_{id}',
                                 label_visibility='collapsed')

    with col2: # 삭제 버튼
       if st.button('삭제', key=f"del_{id}"):
          delete_university(id)
          st.toast(f"'{un}' 목록에서 제거되었습니다.")
          st.rerun()

def print_search_results(results):
    if len(results)==0:
        st.warning('검색 결과가 없습니다.')
        return
    st.subheader('\n-------대학교 검색 결과------')
    for index, university in enumerate(results, start=1):
        st.success(f"{index}. " f"{university['region']} / " f"{university['un']}")
      #   col_info, col_save = st.columns([4, 1])
      #   with col_info:
      #      st.markdown(f"{index}. " f"{book['title']} / " f"{book['author']}")
      #   with col_save:
      #      if st.button("내 서재에 저장", key=f"save_{index}", use_container_width=True):
      #          try:
      #             add_book(book['title'], book['author'])
      #             st.toast(f"'{title}'이(가) 내 서재에 저장되었습니다.")
      #          except Exception as e:
      #             st.error(f"저장 실패: {e}")
      #   st.divider()
              

        


st.set_page_config(page_title='대학교 기록 관리 시스템', page_icon='📚')

st.sidebar.title('대학교 기록 관리')
st.sidebar.write('나만의 대학교 기록을 관리해보세요.')

menu = st.sidebar.radio("메뉴 선택", 
                ['내 대학교 (목록/관리)', '내 대학교 평점 입력', '직접 대학교 검색 및 저장', '외부 대학교 검색 및 등록'])

if menu == '내 대학교 (목록/관리)':
    st.header('📖🏫 내 대학교')
    st.write('저장된 대학교를 조회하고 대학교 평점 수정 및 삭제를 관리할 수 있습니다. ')

    keyword = st.text_input('내 대학교 검색(대학교 이름)', placeholder='검색어 입력')

    if keyword.strip():
        rows = search_uns(keyword.strip())
    else:
        rows = get_all_uns()
    print_uns(rows, )


elif menu == '내 대학교 평점 입력':
   st.header('✨내 대학교 평점 입력')
   st.write('평점을 입력하거나 수정할 수 있습니다.')
   rows = []
   for row in rows:
    id = row[0]
    region = row[1]
    un = row[2]
    rating = row[3]
   
   if rating == 0: rating_text = '평점 없음'
   else: rating_text = f"{rating}점"
   
   st.write(f'{id}./ {un} / {region} / {rating_text}')
   
   col1, col2 = st.columns([1, 2])
   
   with col1: # 평점
      current_rate = rating if 1<=rating<=5 else 1
      new_rating = st.selectbox('평점', options=[1,2,3,4,5],
                              index=current_rate-1,
                              key=f'rate_sel_{id}',
                              label_visibility='collapsed')
   with col2: # 평점 수정 버튼
      if st.button('평점 저장', key=f'rate_btn_{id}'):
         update_rating(id, new_rating)
         st.toast(f"'{un}'의 평점이 수정되었습니다.")
         st.rerun()



elif menu== '직접 대학교 검색 및 저장':
    st.header('➕ 직접 도서 등록')
    st.write('대학교의 정보를 직접 등록하세요. ')

    with st.form('add_university_form', clear_on_submit=True):
       region = st.text_input('지역명 *', placeholder='지역명을 입력하세요.')
       un = st.text_input('대학교 *', placeholder='대학교명을 입력하세요.')
       address = st.text_input('주소 *', placeholder='주소를 입력하세요.')
       Ft = st.text_input('설립 유형 *', placeholder='설립 유형을 입력하세요.')
       submitted = st.form_submit_button('내 대학교 목록에 등록', use_container_width=True)

       if submitted:
          if not region.strip() or not un.strip() or address.strip() or Ft.strip():
             st.warning('지역과 대학교, 설립 유형, 주소를 모두 입력해주세요.')
          
          else:
             add_university(region.strip(), un.strip())
             st.success('내 대학교 목록에 등록되었습니다!')

elif menu== '외부 대학교 검색 및 등록':
    st.header('🔎 외부 대학교 검색 및 등록')
    st.write('외부 대학교 API를 통해 대학교 정보를 검색하고 서재에 저장할 수 있습니다. ')

    search_col, btn_col = st.columns([4, 1])
    with search_col:
       keyword = st.text_input("검색할 대학교 이름", placeholder="예: 서울 대학교", 
                               label_visibility="collapsed")
    with btn_col:
       search_clicked = st.button('대학교 검색', use_container_width=True)

    if search_clicked:
       if not keyword.strip():
          st.warning("검색어를 입력해주세요.")
       else:
          try:
            results = search_external_uns(keyword.strip())
            st.session_state["search_results"] = results
          except Exception as e:
            st.error(f"검색 중 오류가 발생했습니다. {e}")
            st.session_state['search_results'] = []
    if "search_results" in st.session_state:
       results = st.session_state["search_results"]
       print_search_results(results)




