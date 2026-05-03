"""通知异步任务"""
from celery import shared_task


@shared_task(queue='notify')
def send_notification(ntype, title, message, device_id=None, send_email=False):
    """发送通知"""
    from .models import Notification, EmailConfig

    # 站内通知
    Notification.objects.create(
        type=ntype,
        title=title,
        message=message,
        device_id=device_id,
    )

    # 邮件通知
    if send_email:
        config = EmailConfig.objects.filter(enabled=True).first()
        if config:
            try:
                import smtplib
                from email.mime.text import MIMEText
                msg = MIMEText(message, 'plain', 'utf-8')
                msg['Subject'] = f'[BeeAdmin] {title}'
                msg['From'] = config.sender_email
                # TODO: 收件人配置
                # msg['To'] = ...
                # server = smtplib.SMTP_SSL(config.smtp_host, config.smtp_port)
                # server.login(config.sender_email, config.sender_password)
                # server.send_message(msg)
                # server.quit()
            except Exception as e:
                print(f'邮件发送失败: {e}')
