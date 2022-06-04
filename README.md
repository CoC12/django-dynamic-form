# Django Dynamic Form

Django Dynamic Form は、ユーザーによるフォームの入力、選択、変更などのイベントを検知し、
各フィールドの表示/非表示、有効/無効の切り替えや選択肢の変更などのフォームの最新化を行います。

## Installation

1. pip を使いインストールします。

    ```
    pip install django-dynamic-form
    ```

2. `'dynamic_form'` を `INSTALLED_APPS` に追加します。

   ```python
   INSTALLED_APPS = [
       ...
       'dynamic_form',
   ]
   ```

3. dynamic_form の URLconf をプロジェクトの `urls.py` に追加します。

   ```python
   urlpatterns = [
       ...
       path('', include('dynamic_form.urls')),
   ]
   ```

4. HTML に script タグを追加します。

   ```html
   {% load static %}
   <script type="text/javascript" src="{% static 'dynamic_form/js/dynamic-form.js' %}"></script>
   ```

## Quick start

1. フォーム に `DynamicFormMixin` を継承させます。

    ```python
    from django import forms
    from dynamic_form.forms import DynamicFormMixin


    class TestForm(DynamicFormMixin, forms.Form):
        ...
    ```

2. `settings.py` にフォームへの`.(ドット)`区切りのモジュールパスと、フォームを一意に特定する文字列を定義します。

    ```python
    DYNAMIC_FORM = {
        'FORM_KEYS': {
            'sample_app.forms.TestForm': 'test_form',
        },
    }
    ```

3. フォーム最新化のトリガーとなるフィールドに、data 属性 `data-ddf-trigger` を追加します。
属性値にはイベントの種類を表す`TriggerEventTypes`クラスのメンバー値を指定します。
詳細は[TriggerEventTypes](#triggereventtypes)をご覧ください。

    ```python
    from dynamic_form.types import TriggerEventTypes


    class TestForm(DynamicFormMixin, forms.Form):
        age = forms.IntegerField(
            label='年齢',
            widget=forms.NumberInput(
                attrs={
                    'data-ddf-trigger': TriggerEventTypes.BLUR,
                }
            )
        )
    ```

4. 表示/非表示、有効/無効の切り替えなど、フィールドに対する制御を定義します。
詳細は[フィールド制御メソッド](#フィールド制御メソッド)をご覧ください。

    ```python
    class TestForm(DynamicFormMixin, forms.Form):
        age = forms.IntegerField(
            label='年齢',
            widget=forms.NumberInput(
                attrs={
                    'data-ddf-trigger': TriggerEventTypes.BLUR,
                }
            )
        )
        consent = forms.BooleanField(
            label='保護者同意',
            help_text='未成年の場合は保護者の同意が必要です。',
        )

        def is_hidden_consent(self):
            age = self.data.get('age', '')
            return int(age) >= 20 if age.isdigit() else True
    ```

5. ビューでフォームを生成し、`render_form()` メソッドの戻り値をテンプレートに渡します。
テンプレートに渡された `render_form()` メソッドの戻り値を`form`タグで囲み、`method` を `POST` にします。

    ```python
    class TestView(TemplateView):
        template_name = 'test_view.html'

        def get(self, request, *args, **kwargs):
            form = TestForm()
            context = {
                'test_form': form.render_form(),
            }
            return self.render_to_response(context)
    ```

    test_view.html

    ```html
    <form method="post">
        {% csrf_token %}
        {{ test_form }}
        <input type="submit" value="Submit" />
    </form>
    ```

## Documentation

### **DynamicFormMixin**

#### クラス変数

* form_template

    フォームの表示はテンプレートファイルによりカスタマイズできます。
    このテンプレートには `form` タグを含めません。
    カスタマイズしたテンプレートファイルは `form_template` で指定します。

    ```python
    class TestForm(DynamicFormMixin, forms.Form):
        form_template = 'sample_app/sample_form.html'
    ```

    sample_app/sample_form.html

    ```html
    {% for field in form.visible_fields %}
        <div class="form-row">
            <div class="form-label">
                {{ field.label }}
            </div>
            <div class="form-field">
                {{ field }}
            </div>
            {% if field.errors %}
            <div class="form-error">
                {{ field.errors }}
            </div>
            {% endif %}
        </div>
    {% endfor %}
    ```

* do_dynamic_validate

    フォーム最新化のときに、バリデーションを実施するかを指定します。
    デフォルトは `False` です。

    ```python
    class TestForm(DynamicFormMixin, forms.Form):
        do_dynamic_validate = True
    ```

#### フィールド制御メソッド

フィールド制御メソッドは、各フィールドの表示/非表示、有効/無効の切り替えや選択肢の変更などを制御します。
制御が必要なフィールドの、必要なメソッドのみを定義します。
フォームの入力内容は `self.data` からアクセスできますが、未入力のフィールドなど値が `self.data` に含まれない可能性を考慮する必要があります。

制御できる項目は以下のとおりです。

* is_hidden_<field_name>()

    フィールドを非表示にするかの真偽値を返します。
    `True` を返した場合、フィールドの `required` が `False` に、 ウィジェットが `django.forms.HiddenInput` となります。

* is_disabled_<field_name>()

    フィールドを無効にするかの真偽値を返します。
    `True` を返した場合、フィールドの `disabled` が `True` に、 `required` が `False` となります。

* is_required_<field_name>()

    フィールドを必須にするかの真偽値を返します。
    `True` を返した場合、フィールドの `required` が `True` となります。

* set_queryset_<field_name>()

    フィールドに設定する `queryset` を返します。 `ModelChoiceField` に対して使用します。

    ```python
    def set_queryset_task(self):
        selected_member = self.data.get('member')
        return Task.objects.filter(id=selected_member)
    ```

* set_choices_<field_name>()

    フィールドに設定する `choices` を返します。 `ChoiceField` に対して使用します。

    ```python
    def set_choices_fruits(self):
        return [
            (1, 'apple'),
            (2, 'banana'),
            (3, 'melon'),
        ]
    ```

### **TriggerEventTypes**

TriggerEventTypesでは、フォーム最新化のトリガーとなるイベントを定義しています。
フィールドの `data-ddf-trigger` 属性の属性値に指定します。

* BLUR

    フィールドから `blur` イベントが発生した場合にフォームを最新化します。

* CHANGE

    フィールドから `change` イベントが発生した場合にフォームを最新化します。

* CLICK

    フィールドから `click` イベントが発生した場合にフォームを最新化します。

* DOUBLE_CLICK

    フィールドから `dblclick` イベントが発生した場合にフォームを最新化します。

* INPUT

    フィールドから `input` イベントが発生した場合にフォームを最新化します。

* KEY_UP

    フィールドから `keyup` イベントが発生した場合にフォームを最新化します。

* KEY_DOWN

    フィールドから `keydown` イベントが発生した場合にフォームを最新化します。

* SELECT

    フィールドから `select` イベントが発生した場合にフォームを最新化します。


### **Settings**

Django Dynamic Form の設定は `DYNAMIC_FORM` という名前で指定します。

```python
DYNAMIC_FORM = {
    'FORM_KEYS': {
        'sample_app.forms.TestForm': 'test_form',
    },
}
```

* FORM_KEYS

    フォームへの`.(ドット)`区切りのモジュールパスと、フォームを一意に特定する文字列を定義します。
    この文字列はHTML上に `data-form-key` 属性の属性値として設定されます。

    モジュールパスは `__class__.__module__` と `__class__.__name__` を`.(ドット)`区切りで連結した文字列です。
