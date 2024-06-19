import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import MailRequestSerializer
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class SendMailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = MailRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            product_number = serializer.validated_data['product_number']
            product_name = serializer.validated_data['product_name']
            text = serializer.validated_data['text']
            file = request.FILES.get('file')

            send_email = os.getenv("SEND_EMAIL")
            send_pwd = os.getenv("SEND_PWD")
            recv_email = os.getenv("RECV_EMAIL")

            smtp_name = "smtp.naver.com"
            smtp_port = 587

            try:
                msg = MIMEMultipart()
                msg['Subject'] = 'HealtyFood 챗봇 문의'
                msg['From'] = send_email
                msg['To'] = recv_email

                body_content = f"Phone Number: {phone_number}\nProduct Number: {product_number}\nProduct Name: {product_name}\n\n{text}"
                body = MIMEText(body_content, 'plain', 'utf-8')
                msg.attach(body)

                if file:
                    part = MIMEApplication(file.read(), Name=file.name)
                    part['Content-Disposition'] = f'attachment; filename="{file.name}"'
                    msg.attach(part)

                with smtplib.SMTP(smtp_name, smtp_port) as server:
                    server.starttls()
                    server.login(send_email, send_pwd)
                    server.sendmail(send_email, recv_email, msg.as_string())

                return Response({"message": "문의사항이 접수되었습니다."}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)