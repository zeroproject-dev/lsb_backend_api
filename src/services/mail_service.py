import os
import smtplib
from email.message import EmailMessage

from flask.templating import render_template


def send_create_account(user):
    subject = "Confirmación de cuenta"
    name = user['name']
    data = {
        'app_url': 'https://lsb.zeroproject.dev/',
        'header': f'Hola, {name},',
        'body': 'Para finalizar la creación de tu cuenta debes ingresar a la siguiente página presionando el siguiente botón:',
        'button': 'Finalizar registro',
        'button_link': 'https://lsb.zeroproject.dev'
    }
    body = render_template('mail.html', **data)
    return send_mail(user['email'], subject, body)


def send_mail(email, subject, body):
    em = EmailMessage()
    em['From'] = str(os.getenv('EMAIL_FROM'))
    em['To'] = email
    em['Subject'] = subject
    em.set_content(body)

    try:
        port = int(str(os.getenv('SMTP_PORT')))
        with smtplib.SMTP(str(os.getenv('SMTP_SERVER')), port) as smtp:
            smtp.login(str(os.getenv('SMTP_USER')),
                       str(os.getenv('SMTP_PASSWORD')))
            smtp.sendmail(em['from'], email, em.as_string())
        return True
    except Exception as e:
        print(e)
        return False


def get_body(link, title):
    header = """
<!DOCTYPE html
  PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office">

<head>
  <meta charset="UTF-8">
  <meta content="width=device-width, initial-scale=1" name="viewport">
  <meta name="x-apple-disable-message-reformatting">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta content="telephone=no" name="format-detection">
  <title>Correo</title><!--[if (mso 16)]>
<style type="text/css">
a {text-decoration: none;}
</style>
<![endif]--><!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--><!--[if gte mso 9]>
<xml>
<o:OfficeDocumentSettings>
<o:AllowPNG></o:AllowPNG>
<o:PixelsPerInch>96</o:PixelsPerInch>
</o:OfficeDocumentSettings>
</xml>
<![endif]-->
  <style type="text/css">
    .rollover:hover .rollover-first {
      max-height: 0px !important;
      display: none !important;
    }

    .rollover:hover .rollover-second {
      max-height: none !important;
      display: inline-block !important;
    }

    .rollover div {
      font-size: 0px;
    }

    u~div img+div>div {
      display: none;
    }

    #outlook a {
      padding: 0;
    }

    span.MsoHyperlink,
    span.MsoHyperlinkFollowed {
      color: inherit;
      mso-style-priority: 99;
    }

    a.es-button {
      mso-style-priority: 100 !important;
      text-decoration: none !important;
    }

    a[x-apple-data-detectors] {
      color: inherit !important;
      text-decoration: none !important;
      font-size: inherit !important;
      font-family: inherit !important;
      font-weight: inherit !important;
      line-height: inherit !important;
    }

    .es-desk-hidden {
      display: none;
      float: left;
      overflow: hidden;
      width: 0;
      max-height: 0;
      line-height: 0;
      mso-hide: all;
    }

    .es-button-border:hover>a.es-button {
      color: #ffffff !important;
    }

    @media only screen and (max-width:600px) {
      *[class="gmail-fix"] {
        display: none !important
      }

      p,
      a {
        line-height: 150% !important
      }

      h1,
      h1 a {
        line-height: 120% !important
      }

      h2,
      h2 a {
        line-height: 120% !important
      }

      h3,
      h3 a {
        line-height: 120% !important
      }

      h4,
      h4 a {
        line-height: 120% !important
      }

      h5,
      h5 a {
        line-height: 120% !important
      }

      h6,
      h6 a {
        line-height: 120% !important
      }

      h1 {
        font-size: 30px !important;
        text-align: left;
        line-height: 120% !important
      }

      h2 {
        font-size: 26px !important;
        text-align: left;
        line-height: 120% !important
      }

      h3 {
        font-size: 20px !important;
        text-align: left;
        line-height: 120% !important
      }

      h4 {
        font-size: 24px !important;
        text-align: left
      }

      h5 {
        font-size: 20px !important;
        text-align: left
      }

      h6 {
        font-size: 16px !important;
        text-align: left
      }

      .es-header-body h1 a,
      .es-content-body h1 a,
      .es-footer-body h1 a {
        font-size: 30px !important
      }

      .es-header-body h2 a,
      .es-content-body h2 a,
      .es-footer-body h2 a {
        font-size: 26px !important
      }

      .es-header-body h3 a,
      .es-content-body h3 a,
      .es-footer-body h3 a {
        font-size: 20px !important
      }

      .es-header-body h4 a,
      .es-content-body h4 a,
      .es-footer-body h4 a {
        font-size: 24px !important
      }

      .es-header-body h5 a,
      .es-content-body h5 a,
      .es-footer-body h5 a {
        font-size: 20px !important
      }

      .es-header-body h6 a,
      .es-content-body h6 a,
      .es-footer-body h6 a {
        font-size: 16px !important
      }

      .es-menu td a {
        font-size: 14px !important
      }

      .es-header-body p,
      .es-header-body a {
        font-size: 14px !important
      }

      .es-content-body p,
      .es-content-body a {
        font-size: 14px !important
      }

      .es-footer-body p,
      .es-footer-body a {
        font-size: 14px !important
      }

      .es-infoblock p,
      .es-infoblock a {
        font-size: 12px !important
      }

      .es-m-txt-c,
      .es-m-txt-c h1,
      .es-m-txt-c h2,
      .es-m-txt-c h3,
      .es-m-txt-c h4,
      .es-m-txt-c h5,
      .es-m-txt-c h6 {
        text-align: center !important
      }

      .es-m-txt-r,
      .es-m-txt-r h1,
      .es-m-txt-r h2,
      .es-m-txt-r h3,
      .es-m-txt-r h4,
      .es-m-txt-r h5,
      .es-m-txt-r h6 {
        text-align: right !important
      }

      .es-m-txt-j,
      .es-m-txt-j h1,
      .es-m-txt-j h2,
      .es-m-txt-j h3,
      .es-m-txt-j h4,
      .es-m-txt-j h5,
      .es-m-txt-j h6 {
        text-align: justify !important
      }

      .es-m-txt-l,
      .es-m-txt-l h1,
      .es-m-txt-l h2,
      .es-m-txt-l h3,
      .es-m-txt-l h4,
      .es-m-txt-l h5,
      .es-m-txt-l h6 {
        text-align: left !important
      }

      .es-m-txt-r img,
      .es-m-txt-c img,
      .es-m-txt-l img {
        display: inline !important
      }

      .es-m-txt-r .rollover:hover .rollover-second,
      .es-m-txt-c .rollover:hover .rollover-second,
      .es-m-txt-l .rollover:hover .rollover-second {
        display: inline !important
      }

      .es-m-txt-r .rollover div,
      .es-m-txt-c .rollover div,
      .es-m-txt-l .rollover div {
        line-height: 0 !important;
        font-size: 0 !important
      }

      .es-spacer {
        display: inline-table
      }

      a.es-button,
      button.es-button {
        font-size: 20px !important
      }

      a.es-button,
      button.es-button {
        display: inline-block !important
      }

      .es-button-border {
        display: inline-block !important
      }

      .es-m-fw,
      .es-m-fw.es-fw,
      .es-m-fw .es-button {
        display: block !important
      }

      .es-m-il,
      .es-m-il .es-button,
      .es-social,
      .es-social td,
      .es-menu {
        display: inline-block !important
      }

      .es-adaptive table,
      .es-left,
      .es-right {
        width: 100% !important
      }

      .es-content table,
      .es-header table,
      .es-footer table,
      .es-content,
      .es-footer,
      .es-header {
        width: 100% !important;
        max-width: 600px !important
      }

      .adapt-img {
        width: 100% !important;
        height: auto !important
      }

      .es-mobile-hidden,
      .es-hidden {
        display: none !important
      }

      .es-desk-hidden {
        width: auto !important;
        overflow: visible !important;
        float: none !important;
        max-height: inherit !important;
        line-height: inherit !important
      }

      tr.es-desk-hidden {
        display: table-row !important
      }

      table.es-desk-hidden {
        display: table !important
      }

      td.es-desk-menu-hidden {
        display: table-cell !important
      }

      .es-menu td {
        width: 1% !important
      }

      table.es-table-not-adapt,
      .esd-block-html table {
        width: auto !important
      }

      .es-social td {
        padding-bottom: 10px
      }

      .h-auto {
        height: auto !important
      }

      p,
      ul li,
      ol li,
      a {
        font-size: 16px !important
      }

      h1 a {
        text-align: left
      }

      h2 a {
        text-align: left
      }

      h3 a {
        text-align: left
      }

      a.es-button {
        border-left-width: 0px !important;
        border-right-width: 0px !important
      }
    }
  </style>
</head>

<body style="width:100%;height:100%;padding:0;Margin:0">
  <div class="es-wrapper-color" style="background-color:#EFEFEF"><!--[if gte mso 9]>
<v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t">
<v:fill type="tile" color="#efefef"></v:fill>
</v:background>
<![endif]-->
    <table class="es-wrapper" width="100%" cellspacing="0" cellpadding="0"
      style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-repeat:repeat;background-position:center top;background-color:#EFEFEF">
      <tr>
        <td valign="top" style="padding:0;Margin:0">
          <table cellpadding="0" cellspacing="0" class="es-header" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
              <td align="center" style="padding:0;Margin:0">
                <table class="es-header-body" cellspacing="0" cellpadding="0" align="center"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#E6EBEF;width:600px">
                  <tr>
                    <td align="left" bgcolor="#FFE6CF" style="padding:20px;Margin:0;background-color:#FFE6CF">
                      <table width="100%" cellspacing="0" cellpadding="0"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                          <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr>
    """

    link_photo = f'<td align="center" style="padding:0;Margin:0;font-size:0"><a href="{link}" target="_blank"'
    before_title = """
                                    style="mso-line-height-rule:exactly;text-decoration:none;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:14px;color:#677D9E"><img
                                      src="https://ebblibj.stripocdn.email/content/guids/CABINET_8eaa0a7f951420b8062c116f17cfefe0bc87ba80a16e9befc18a758233e5bd8c/images/_bde7a413a9494363b10ed227d4d2c6f0removebgpreview.png"
                                      alt="Logo" title="Logo" width="120"
                                      style="display:block;font-size:14px;border:0;outline:none;text-decoration:none"></a>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table class="es-content" cellspacing="0" cellpadding="0" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
            <tr>
              <td align="center" bgcolor="transparent" style="padding:0;Margin:0;background-color:transparent">
                <table class="es-content-body" cellspacing="0" cellpadding="0" bgcolor="#ffffff" align="center"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;width:600px">
                  <tr>
                    <td align="left" bgcolor="#222246" style="padding:40px;Margin:0;background-color:#222246">
                      <table cellspacing="0" cellpadding="0" align="right" class="es-right"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                        <tr>
                          <td valign="top" align="center" style="padding:0;Margin:0;width:520px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
    """

    return header + link_photo + before_title + """
                              <tr>
                                <td align="left" style="padding:0;Margin:0">
                                  <h3
                                    style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:20px;font-style:normal;font-weight:normal;line-height:24px;color:#666666">
                                    <span style="color:#efefef">
                                      TITLE
                                    </span><br>
                                  </h3>
                                </td>
                              </tr>
                              <tr>
                                <td align="left" style="padding:0;Margin:0;padding-top:15px">
                                  <p
                                    style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;letter-spacing:0;color:#efefef;font-size:14px">
                                    BODY
                                  </p>
                                </td>
                              </tr>
                              <tr>
                                <td align="center" style="padding:0;Margin:0;padding-top:30px"><span
                                    class="es-button-border"
                                    style="border-style:solid;border-color:transparent;background:#2CB543;border-width:0px;display:inline-block;border-radius:0px;width:auto"><a
                                      href="LINK" class="es-button" target="_blank"
                                      style="mso-style-priority:100 !important;text-decoration:none !important;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;font-size:16px;color:#FFFFFF;padding:10px 20px 10px 20px;display:inline-block;background:#8598B2;border-radius:0px;font-weight:normal;font-style:normal;line-height:19px !important;width:auto;text-align:center;letter-spacing:0;mso-padding-alt:0;mso-border-alt:10px solid #8598B2">
                                      BUTTON
                                    </a></span>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table cellpadding="0" cellspacing="0" class="es-footer" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important;background-color:transparent;background-repeat:repeat;background-position:center top">
            <tr>
              <td align="center" style="padding:0;Margin:0">
                <table class="es-footer-body" cellspacing="0" cellpadding="0" align="center"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#E6EBEF;width:600px">
                  <tr>
                    <td align="left" bgcolor="#FFE6CF" style="padding:0;Margin:0;background-color:#FFE6CF">
                      <!--[if mso]><table style="width:600px" cellpadding="0" cellspacing="0"><tr><td style="width:142px" valign="top"><![endif]-->
                      <table cellspacing="0" cellpadding="0" align="left" class="es-left"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:left">
                        <tr>
                          <td valign="top" align="center" style="padding:0;Margin:0;width:142px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr>
                                <td align="center" style="padding:0;Margin:0;font-size:0"><img class="adapt-img"
                                    src="https://ebblibj.stripocdn.email/content/guids/CABINET_8eaa0a7f951420b8062c116f17cfefe0bc87ba80a16e9befc18a758233e5bd8c/images/_bde7a413a9494363b10ed227d4d2c6f0.jpeg"
                                    alt="" width="142"
                                    style="display:block;font-size:14px;border:0;outline:none;text-decoration:none">
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                      <!--[if mso]></td><td style="width:0px"></td><td style="width:458px" valign="top"><![endif]-->
                      <table cellpadding="0" cellspacing="0" class="es-right" align="right"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;float:right">
                        <tr>
                          <td align="left" style="padding:0;Margin:0;width:458px">
                            <table cellpadding="0" cellspacing="0" width="100%" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr>
                                <td align="center" style="padding:0;Margin:0">
                                  <h1
                                    style="Margin:0;font-family:arial, 'helvetica neue', helvetica, sans-serif;mso-line-height-rule:exactly;letter-spacing:0;font-size:30px;font-style:normal;font-weight:normal;line-height:60px !important;color:#333333">
                                    TRADUCTOR LENGUAJE DE SEÑAS BOLIVIANO</h1>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table><!--[if mso]></td></tr></table><![endif]-->
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
          <table class="es-content" cellspacing="0" cellpadding="0" align="center"
            style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:100%;table-layout:fixed !important">
            <tr>
              <td align="center" style="padding:0;Margin:0">
                <table class="es-content-body"
                  style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:transparent;width:600px"
                  cellspacing="0" cellpadding="0" align="center">
                  <tr>
                    <td align="left" style="padding:0;Margin:0;padding-right:20px;padding-left:20px">
                      <table width="100%" cellspacing="0" cellpadding="0"
                        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                        <tr>
                          <td valign="top" align="center" style="padding:0;Margin:0;width:560px">
                            <table width="100%" cellspacing="0" cellpadding="0" role="presentation"
                              style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px">
                              <tr>
                                <td align="center" style="padding:0;Margin:0">
                                  <p
                                    style="Margin:0;mso-line-height-rule:exactly;font-family:arial, 'helvetica neue', helvetica, sans-serif;line-height:21px;letter-spacing:0;color:#333333;font-size:14px">
                                    ASORPAZ</p>
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </div>
</body>

</html>
    """
