Jackal, the Boilerplate library for Django REST Framework
-------------------------------------------------------------

.. image:: https://badge.fury.io/py/django-jackal.svg
    :target: https://badge.fury.io/py/django-jackal

.. image:: https://github.com/joyongjin/Jackal/raw/master/images/jackal.jpg
    :width: 720px
    :align: center


**Jackal** 은 웹 백엔드 서버에서 필요한 기능들을 손쉽게 구현하도록 도와주는 Django 및 Django REST Framework(DRF) 기반 Boilerplate Library 입니다.

**Jackal** 의 특징:

* 모델 아이템의 생성, 조회, 수정, 삭제 및 페이지네이션 등의 구현을 돕는 Generic API Views.
* GET query parameter 기반의 직관적인 필터링.
* POST body 값을 모델 친화적으로 검증.
* API View 확장성 증가

Installation
===============

현재 베타 배포 상태. 라이브러리의 완전한 검증이 이루어지지 않았기에, 버그가 다수 발생 가능성이 높습니다.


.. code::

    pip install django-jackal


Document
============

자세한 사항은 위키_ 참조

.. _위키: https://github.com/joyongjin/jackal/wiki

Test
============

.. code::

    python runtests.py tests
