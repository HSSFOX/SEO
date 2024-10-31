from PyQt5 import QtCore, QtWidgets, QtNetwork, QtWebEngineWidgets


def set_ssl_protocol():
    default_config = QtNetwork.QSslConfiguration.defaultConfiguration()
    default_config.setProtocol(QtNetwork.QSsl.TlsV1_2)
    QtNetwork.QSslConfiguration.setDefaultConfiguration(default_config)


class WebEnginePage(QtWebEngineWidgets.QWebEnginePage):
    def certificateError(self, certificateError):
        print(certificateError.errorDescription(), certificateError.url(), certificateError.isOverridable())
        error = certificateError.error()
        if error == QtWebEngineWidgets.WebEngineCertificateError.SslPinnedKeyNotInCertificateChain:
            print("SslPinnedKeyNotInCertificateChain")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateCommonNameInvalid:
            print("CertificateCommonNameInvalid")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateDateInvalid:
            print("CertificateDateInvalid")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateAuthorityInvalid:
            print("CertificateAuthorityInvalid")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateContainsErrors:
            print("CertificateContainsErrors")
        if error == QtWebEngineWidgets.WebEngineCertificateError.CertificateNoRevocationMechanism:
            print("CertificateNoRevocationMechanism")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateUnableToCheckRevocation:
            print("CertificateUnableToCheckRevocation")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateRevoked:
            print("CertificateRevoked")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateInvalid:
            print("CertificateAuthorityInvalid")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateWeakSignatureAlgorithm:
            print("CertificateWeakSignatureAlgorithm")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateNonUniqueName:
            print("CertificateNonUniqueName")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateWeakKey:
            print("CertificateWeakKey")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateNameConstraintViolation:
            print("CertificateNameConstraintViolation")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateValidityTooLong:
            print("CertificateValidityTooLong")
        elif error == QtWebEngineWidgets.WebEngineCertificateError.CertificateTransparencyRequired:
            print("CertificateTransparencyRequired")

        return super(WebEnginePage, self).certificateError(certificateError)