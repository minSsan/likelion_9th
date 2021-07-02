from django.db import models

class Medical(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

class Detail(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

class hospital(models.Model):
    Name = models.TextField()
    Addr = models.TextField()
    Tele = models.TextField()
    Mono = models.TextField(blank=True, null=True)
    Monc = models.TextField(blank=True, null=True)
    Tueo = models.TextField(blank=True, null=True)
    Tuec = models.TextField(blank=True, null=True)
    Wedo = models.TextField(blank=True, null=True)
    Wedc = models.TextField(blank=True, null=True)
    Thuo = models.TextField(blank=True, null=True)
    Thuc = models.TextField(blank=True, null=True)
    Frio = models.TextField(blank=True, null=True)
    Fric = models.TextField(blank=True, null=True)
    Sato = models.TextField(blank=True, null=True)
    Satc = models.TextField(blank=True, null=True)
    Suno = models.TextField(blank=True, null=True)
    Sunc = models.TextField(blank=True, null=True)
    Holo = models.TextField(blank=True, null=True)
    Holc = models.TextField(blank=True, null=True)
    Hpid = models.TextField()
    Etc = models.TextField(blank=True, null=True)
    Info = models.TextField(blank=True, null=True)
    Map = models.TextField(blank=True, null=True)

    Todr = models.TextField(blank=True, null=True) #총 의사 수
    medr = models.TextField(blank=True, null=True) #의과 전문의
    dedr = models.TextField(blank=True, null=True) #치과 전문의
    cmdr = models.TextField(blank=True, null=True) #한방 전문의

    hgSi = models.TextField(blank=True, null=True) #일반입원실 상급병상
    stSi = models.TextField(blank=True, null=True) #일반입원실 일반병상
    adSp = models.TextField(blank=True, null=True) #성인중환자 병상
    nbSp = models.TextField(blank=True, null=True) #신생아중환자 병상
    paCn = models.TextField(blank=True, null=True) #분만실 병상
    soCn = models.TextField(blank=True, null=True) #수술실 병상
    emCn = models.TextField(blank=True, null=True) #응급실 병상
    ptCn = models.TextField(blank=True, null=True) #물리치료실 병상
    chCn = models.TextField(blank=True, null=True) #소아중환자 병상
    pshgCn = models.TextField(blank=True, null=True) #정신과 폐쇄상급병상
    psstCn = models.TextField(blank=True, null=True) #정신과 페쇄일반병상
    isCn = models.TextField(blank=True, null=True) #격리병상
    anCn = models.TextField(blank=True, null=True) #무균치료실 병상

    emDy = models.TextField(blank=True, null=True) #주간 응급실 운영 여부
    emNg = models.TextField(blank=True, null=True) #야간 응급실 운영 여부
    paQt = models.TextField(blank=True, null=True) #주차 가능 대수
    dgsb = models.TextField(blank=True, null=True) #진료가능 과목
    srch = models.TextField(blank=True, null=True) #전문병원지정분야
    

    def __str__(self):
        return self.Name