from django.db import models





class EmailSendLog(models.Model):
    emailto = models.CharField('Recipient', max_length=300)
    title = models.CharField('mail title', max_length=2000)
    content = models.TextField('content of email')
    send_result = models.BooleanField('result', default=False)
    created_time = models.DateTimeField('Create time', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Mail Send log'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']
