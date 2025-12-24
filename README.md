<img width="1919" height="910" alt="image" src="https://github.com/user-attachments/assets/204537ba-237e-4bca-a3d8-5c9296471a0c" /># 🪐 NASA Exoplanet Analytics: Habitable Worlds Explorer

> **"Are we alone?"** (Yalnız mıyız?) sorusuna veri bilimi ve astrofizik ile cevap arayan interaktif bir dashboard projesi.

Bu proje, NASA'nın **Habitable Worlds Catalog (HWC DATA)** arşivini kullanarak, Dünya'ya en çok benzeyen ve yaşanabilir olma ihtimali en yüksek ötegezegenleri analiz eder, kategorize eder ve görselleştirir.

## 🚀 Proje Hakkında

Bu çalışma iki ana katmandan oluşur:
1. **Veri Mühendisliği (SQL):** BigQuery üzerinde ham NASA verisinin filtrelenmesi ve 5 farklı kategoriye ayrılması.
2. **Görselleştirme & Fizik (Python):** Streamlit ve Three.js kullanılarak oluşturulan, anlık gök mekaniği hesaplamaları içeren interaktif arayüz.

---

## 💾 1. Veri Kaynağı ve SQL Analizi

Veriler, `NASA_Exoplanet_Archive.HWC DATA` tablosundan çekilmiştir. Ham veri üzerinde **BigQuery SQL** kullanılarak özel filtreleme algoritmaları uygulandı ve gezegenler 5 ana stratejik gruba ayrıldı:

### 🔍 Oluşturulan Gezegen Grupları:

1.  **Komşular (The Neighbors):** Bize en yakın (5 Parsec altı), Dünya boyutlarında ve yaşanabilir bölgedeki gezegenler.
2.  **TRAPPIST Sistemi:** Bilim dünyasında büyük yankı uyandıran, çoklu gezegen sistemi TRAPPIST-1 ailesi.
3.  **Modern Keşifler (Kepler Era):** 2015 ve sonrasında keşfedilen, ESI (Dünya Benzerlik İndeksi) skoru 0.82'nin üzerinde olan "yeni nesil" adaylar.
4.  **Süper Dünyalar (Super Earths):** Kütlesi Dünya'dan büyük ama yaşanabilir bölgede olan (LHS serisi gibi) dev kayalıklar.
5.  **Tarihi Efsaneler:** Exoplanet keşif tarihinin dönüm noktaları (2011, 2013, 2014 yıllarının en iyi adayları).

*Sorgu mantığında `P_ESI` (Benzerlik İndeksi), `P_RADIUS` (Yarıçap) ve `S_DISTANCE` (Yıldıza Uzaklık) parametreleri optimize edilmiştir.*

---

## 💻 2. Teknoloji ve Özellikler (Python & Streamlit)

Bu dashboard sadece statik verileri göstermez, aynı zamanda **canlı astrofizik hesaplamaları** yapar.

### 🛠 Kullanılan Teknolojiler
* **Python 3.9+**
* **Streamlit:** Web arayüzü ve dashboard yapısı.
* **Pandas:** Veri manipülasyonu.
* **Three.js (JS Entegrasyonu):** 3D interaktif Dünya modeli, atmosfer ve bulut katmanları ile.
* **IP-API & Open-Meteo:** Kullanıcıyı "Yerel İstasyon" olarak algılayıp lokasyon bazlı telemetri verisi sunar.

### 🌟 Öne Çıkan Özellikler

* **Canlı Yörünge Mekaniği:** `datetime` ve trigonometrik fonksiyonlar kullanılarak, Dünya'nın Güneş'e olan anlık uzaklığı (AU ve km cinsinden) ve ışığın ulaşma süresi (dk:sn) gerçek zamanlı hesaplanır.
* **Dinamik ESI Görselleştirmesi:** Her gezegen için renk kodlu (Yeşil/Sarı/Kırmızı) benzerlik barları.
* **Atmosferik 3D Model:** Three.js ile render edilen, kendi ekseni etrafında dönen ve gerçekçi ışıklandırmaya sahip Dünya simülasyonu.
* **Yerel İstasyon Modu:** Kullanıcının IP adresinden konumunu tespit edip, dashboard'u kişisel bir uzay istasyonu terminaline dönüştürür.

---

## 📸 Ekran Görüntüleri
---
<img width="1023" height="1024" alt="Kepler22b" src="https://github.com/user-attachments/assets/6cb45077-2540-4c39-bd7c-f1138379d7e4" />    

![Kepler_442b](https://github.com/user-attachments/assets/ec0e07d0-c50d-44c2-91a1-c7e522177a79)

![Kepler-62f](https://github.com/user-attachments/assets/0148fede-9b37-4c70-9c99-f8c3313d985a)  

![Kepler-186f_Model](https://github.com/user-attachments/assets/cabf1660-628f-4ee5-83bf-02f5f720b109)

<img width="558" height="558" alt="kepler438b" src="https://github.com/user-attachments/assets/1c02a51b-1f6d-49a2-907d-b08573c1ebe1" />

![Kepler-452b_art](https://github.com/user-attachments/assets/1f146ca4-849e-4525-96ca-c492db79fd9a)

![Kepler-1649c](https://github.com/user-attachments/assets/b252c799-7c75-40cf-abdb-35664803bbf3)

![lhs1140b](https://github.com/user-attachments/assets/e162a07c-d814-4947-8ba5-86f78ce00954) ![Proxima-b-](https://github.com/user-attachments/assets/9f02eafc-4120-4503-bb00-9fe1c850c52f)

![ross128b](https://github.com/user-attachments/assets/c18c599d-c75d-4d10-8615-0ae35554d26e) ![teegarden](https://github.com/user-attachments/assets/2b000d69-b15b-4775-a99b-55da0800df74)

<img width="800" height="800" alt="TRAPPIST-1" src="https://github.com/user-attachments/assets/99db2532-ace9-4f34-9efb-ca90edefc0f6" /> ![stars](https://github.com/user-attachments/assets/f50bad6e-7a3d-4b10-a333-5aa182401d19)

## 📦 Kurulum

Projeyi yerel makinenizde çalıştırmak için:

```bash
@echo off
title NASA Uzay Analiz Paneli
color 0B
cls

echo.
echo ========================================================
echo   NASA EXOPLANET ANALYTICS BASLATILIYOR...
echo ========================================================
echo.
echo  [BILGI]
echo  [DURUM]
echo.


python -m streamlit run uzay_analiz.py

pause
