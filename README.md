# healthy-food
<h1>2024.5.1 주의사항</h1>
python manage.py create_groups 명령어 실행 후 회원가입 테스트

모델 변경 사항 있으니 migrate 후 테스트

<h1>2024.5.3 주의사항</h1>
모델 변경 사항 있으니 migrate 후 테스트!! <br>

<br>



![스크린샷 2024-05-03 004213](https://github.com/Gothax/healthy-food/assets/82752784/b68a6317-8392-463e-8c28-67d48ee98e08)
![스크린샷 2024-05-03 004803](https://github.com/Gothax/healthy-food/assets/82752784/232daaae-37f2-4530-8340-1b9e2e8d7d91)
![스크린샷 2024-05-03 004255](https://github.com/Gothax/healthy-food/assets/82752784/86171c32-7657-4069-b008-90db4bedaa57)
![스크린샷 2024-05-03 004232](https://github.com/Gothax/healthy-food/assets/82752784/50e79bb1-744d-487d-9293-67f9d1431b95)



<h1>폴더 구조 5.3 Ver</h1>
apps

- config
- cart

    장바구니 기능 - 세션 이용

    model : X
- feed

    게시물, 리뷰 CRUD, 좋아요


    model : Content, FeedImage, Like, Comment
- follow

    유저간 팔로우, mypage

    일반유저/판매자 유저 구분

    model : Follow

- orders

    주문 생성, 기록 CR

    D 로직 필요 - EX) 3개월 후 파기

    model : Order, OrderItem

- product

    상품 CRUD

    model : Category, Product, ProductImage

- userprofile

    유저 추가 정보(유저 이미지, 닉네임, 주소)

    model : Profile


```

├─cart
│  │  admin.py
│  │  apps.py
│  │  cart.py
│  │  context_processors.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  │
│  ├─templates
│  │  └─cart
│  │          detail.html
│  │
│
├─config
│  │  asgi.py
│  │  forms.py
│  │  settings.py
│  │  urls.py
│  │  views.py
│  │  wsgi.py
│  │  __init__.py
│  │
│
├─feed
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  │
│  ├─templates
│  │  └─feed
│  │          main.html
│  │          post_all.html
│  │          post_create.html
│  │          post_detail.html
│  │          post_edit.html
│  │          review_create.html
│  │          view_user_page.html
│  │
│  ├─templatetags
│  │  │  follow_extras.py
│  │  │
│  │  └─__pycache__
│  │          follow_extras.cpython-310.pyc
│  │
│
├─follow
│  │  admin.py
│  │  apps.py
│  │  forms.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  ├─management
│  │  │  __init__.py
│  │  │
│  │  ├─commands
│  │  │  │  create_groups.py
│  │  │  │  __init__.py
│  │  │  │
│  │
│  ├─templates
│  │  └─follow
│  │          edit_profile.html
│  │          index.html
│  │          seller_page.html
│  │          user_detail.html
│  │
│
├─media
│  │
│  ├─feed_images
│  │
│  └─user_images
│
├─orders
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  │
│  ├─templates
│  │  └─orders
│  │          order_detail.html
│  │          order_history.html
│  │
│
├─product
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  urls.py
│  │  views.py
│  │  __init__.py
│  │
│  │
│  ├─templates
│  │  └─product
│  │          add_product.html
│  │          product_detail.html
│  │          product_list.html
│  │          seller_index.html
│  │
│  ├─templatetags
│  │  │  custom_filters.py
│  │  │  __init__.py
│
├─sales
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│
├─static
│      arrow.png
│      banner.jpg
│      banner1.png
│      banner_2.png
│      carousel.css
│      checkmark.png
│      icon_1.png
│      icon_2.png
│      icon_3.png
│      logo_1.png
│      password_change_form.css
│      register.css
│      sign-in.css
│
├─templates
│  │  base.html
│  │  home.html
│  │
│  └─registration
│          logged_out.html
│          login.html
│          password_change_done.html
│          password_change_form.html
│          register.html
│          register_done.html
│
└─userprofile
    │  admin.py
    │  apps.py
    │  forms.py
    │  models.py
    │  tests.py
    │  views.py
    │  __init__.py
    │
    │
    ├─templates
    │  └─userprofile
```
