# 쇼핑몰 정보 안내 챗봇 웹어플리케이션 "코봇"

저희 조는 서울에서 가장 복잡한 스타필드 코엑스점을 타켓으로 쇼핑몰 정보 안내 챗봇을 구현하였습니다. 
상점들과 주차정보 등 원하는 정보에 대해 간편하게 질의응답할 수 있도록 하였고, 이를 토대로 쇼핑몰 웹사이트를 제작하였습니다. 

## 1. 개발환경
Python                3.6.12  
Django                2.0.2  
gensim                3.8.3  
JPype1                0.7.1  
konlpy                0.5.2  
nltk                  3.4.5  
tensorflow            2.3.0  
Keras                 2.4.3  
java version "1.8.0_261" 


## 2. 제작과정 

### 2.1 홈페이지 작성

HTML로 웹브라우저를 구현한 후, w3schools에서 W3.CSS Template을 사용하여 웹페이지를 디자인하였습니다.
홈페이지 구성은 **홈 / 메뉴얼 / 개발환경 / 팀원소개** 로 나누었고, 오른쪽 하단의 채팅버튼을 클릭하면 챗봇화면으로 이동합니다.
![page_main](https://user-images.githubusercontent.com/68881138/93714766-c6172980-fb9f-11ea-8b23-c032720b004f.jpg)
![page_introduce](https://user-images.githubusercontent.com/68881138/93714821-142c2d00-fba0-11ea-9e0d-222840391d5d.jpg)

### 2.2 크롤링

Selenium 모듈을 사용하여 
 '스타필드 코엑스몰' 사이트에서 '카테고리 안내' 안에 있는 매장 정보들을 세분화하여 크롤링하였습니다.
카테고리 구성은 **레스토랑&카페 / 패션의류 / 패션잡화 / 뷰티 / 라이프스타일 / 홈퍼니싱 / 키즈 / 엔터테인먼트 / 슈퍼마켓/ 서비스**로 되어있고
추가로 **주차정보**에 대하여도 크롤링하였습니다. 


### 2.3 말뭉치 정의
intents 안의 tag,patterns,responses 내용 업데이트하였습니다. 
```
{
        "tag": "CJ푸드몰",
        "patterns": [
          "CJ푸드몰",
          "CJ푸드몰 어디있어요?",
          "CJ푸드몰 알려주세요",
          "CJ푸드몰 뭐있어?",
          "CJ푸드몰 말해줘",
          "CJ푸드몰 찾아줘",
          "CJ푸드몰 찾아주세요",
          "CJ푸드몰 정보",
          "CJ푸드몰 정보 알려줘",
          "CJ푸드몰 가고싶어"
        ],
        "responses": [
          "[임시휴점] 계절밥상<br>위치: B1층<br>대표 전화: 02-1670-0865\n",
          "계절밥상 소반<br>위치: B1층<br>대표 전화: 02-1670-0865\n",
          "방콕9<br>위치: B1층<br>대표 전화: 02-1670-0865\n",
          "빕스마이픽<br>위치: B1층<br>대표 전화: 02-1670-0865\n",
          "제일제면소<br>위치: B1층<br>대표 전화: 02-1670-0865\n",
          "차이나팩토리 익스프레스<br>위치: B1층<br>대표 전화: 1670-0865\n",
          "투썸플레이스<br>위치: B1층<br>대표 전화: 02-1670-0865\n"
        ]
      }
```

### 2.4 딥러닝 학습
 만든 말뭉치를 딥러닝 학습을 시켰습니다. 
챗봇을 실행해보며 patterns를 구체화시키고, 유사도를 바꿔가며 모델학습을 반복하였습니다.

``` python

        # Using Keras, Build neural network(tensorflow2.x로 2020.09.18 변경)
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, input_shape=(len(self.train_x[0]),)),
            tf.keras.layers.Dense(16),
            tf.keras.layers.Dense(len(self.train_y[0]), activation="softmax"),
            ])
        
        model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
        model.fit(self.train_x, self.train_y, epochs=500, batch_size=24)    

```

## 3. 챗봇 사용

가상환경을 실행 후 mychatsite 디렉토리 위치에서 python manage.py runserver를 실행합니다.
```
(tf2_env) C:\Users\A\Desktop\새 폴더\TeamProject\mychatsite>python manage.py runserver
```

### 3.1 카테고리 분류 안내받기
![page_main](https://user-images.githubusercontent.com/68881138/93715163-8ef64780-fba2-11ea-9b64-42dc5800d175.jpg)

ex) 
```
pattern: "레스토랑&카페 알려줘"
response: "CJ푸드몰, 카페/디저트, 한식, 양식, 아시안, 중식, 일식, 퓨전, 분식, 패스트푸드 중에서 하나를 골라주세요"
```

### 3.2 세부카테고리별 매장을 안내받기
ex) 
```
patterns: "한식 매장 어디있어?"
responses: [000, 000, 000, 000, 000, 000, .....]
```

