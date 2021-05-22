from django.db import models

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=100)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/', default="")
    # 업로드된 이미지는 images라는 파일 내에 저장됨

    def __str__(self):
        return self.title

class Comment(models.Model):
    objects = models.Manager()
    blog_id = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    # ForeignKey -> 해당 테이블이 참조할 객체와, 참조 된 객체가 삭제될 때 수행할 동작을 명시
    # CASCADE -> 부모가 삭제되면 자기 자신도 삭제(블로그 글이 삭제 -> 댓글도 삭제)
    # 즉, 특정 Blog 테이블 하나를 불러올거고, 만약 그게 삭제되면 나도 삭제될거야~ 
    date = models.DateTimeField(auto_now_add = True)
    user = models.TextField(max_length = 20)
    content = models.TextField(max_length = 100)