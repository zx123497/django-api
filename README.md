# django-api
## Commit 方式
+ 因為github上設有CI/CD 以及自動化檢查，以pull request方式進行
1. 切換到新的branch (git checkout -b "newbranchname")
2. 將修改的code commit 之後 將此 branch push (git push origin newbranchname)
3. 到github上面發起一個pull request
4. github會進行語法與安全性檢查並且部署到heroku
5. 如果沒有問題 就可以把該branch merge 到 main branch 上

## 環境設定 
+ python pip
+ 環境變數
  + 請在最外層的資料夾中新建.env 然後依照template 中的格式進行填寫
+ 下載套件
  + ```pip install -r requirements.txt```
+ 執行migrate
  + ```python manage.py makemigrations```
  + ```pythom manage.py migrate```
+ 開啟dev server
  + ```python manage.py runserver```
