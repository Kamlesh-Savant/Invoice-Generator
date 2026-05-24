# 📄 Invoice Generator - User Manual (Hinglish)

> **Login Credentials:** Username = `admin`, Password = `1234`

---

## 🏠 1. Dashboard (मुख्य पेज)

Login करते ही Dashboard खुलेगा। यहाँ आपको दिखेगा:

- **कितने Parties** हैं सिस्टम में
- **कितने Invoices** बने हैं
- **कितने Payments** हुए हैं
- **Net Outstanding** = कुल बकाया रकम

नीचे Recent Invoices, Recent Payments और Top Outstanding Parties की लिस्ट दिखेगी।

---

## 👥 2. Party Management (ग्राहक/पार्टी मैनेजमेंट)

**Sidebar में "Parties" पर क्लिक करें.**

### Party कैसे जोड़ें?
1. **Add Party** बटन दबाएं
2. Party Name (ज़रूरी), Mobile, Email, Address भरें
3. **Opening Balance** – अगर party आपको पैसे देती है तो **Positive** डालें, अगर आपको party को देना है तो **Negative** डालें
4. **Save** दबाएं

### Party कैसे खोजें?
- Search बॉक्स में नाम, मोबाइल या email डालें और Search दबाएं

### Party कैसे देखें/एडिट/डिलीट करें?
- हर party के आगे **Edit (✏️)** , **Ledger (📖)** , **Delete (🗑️)** बटन हैं

**Important:** Party डिलीट करने पर उसके सारे Invoices और Payments भी डिलीट हो जाएंगे!

---

## 📄 3. Invoices (बिल बनाना)

**Sidebar में "Invoices" पर क्लिक करें.**

### नया Invoice कैसे बनाएं?
1. **New Invoice** बटन दबाएं
2. **Party सेलेक्ट करें** (ड्रॉपडाउन से)
3. **Date** डालें (आज की date auto आ जाएगी)
4. **Items जोड़ें:**
   - Product/Service का नाम लिखें
   - Quantity (मात्रा) डालें
   - Rate (दर) डालें
   - Amount अपने-आप calculate हो जाएगा (Qty × Rate)
   - **Add Item** दबाकर और items जोड़ सकते हैं
5. **Create Invoice** दबाएं

### Invoice कैसे देखें/प्रिंट करें?
- List में **View (👁️)** बटन दबाएं
- **Download PDF** से PDF डाउनलोड करें
- **Print** से सीधे प्रिंट करें

### Invoice कैसे एडिट/डिलीट करें?
- Edit (✏️) और Delete (🗑️) बटन हर invoice के आगे हैं

> **No Tax System:** इस सिस्टम में GST, CGST, SGST, VAT कुछ नहीं है। सिर्फ Item Amount का Total है।

---

## 💰 4. Payments (भुगतान दर्ज करना)

**Sidebar में "Payments" पर क्लिक करें.**

### Payment कैसे दर्ज करें?
1. **Record Payment** बटन दबाएं
2. **Party सेलेक्ट करें**
3. **Payment Mode चुनें:** Cash, Cheque, Bank Transfer, Online, UPI, Card, Other
4. **Amount डालें**
5. **Reference Number** डालें (जैसे cheque number, UPI ID, transaction ID)
6. **Record Payment** दबाएं

### Payment Receipt PDF
- View पेज पर **Download PDF** से receipt डाउनलोड करें

---

## 📊 5. Ledger (खाता बही / हिसाब किताब)

**यह सबसे ज़रूरी हिस्सा है।**

**Sidebar में "Ledger" पर क्लिक करें.**

### Party का Ledger कैसे देखें?
1. **Party सेलेक्ट करें** ड्रॉपडाउन से
2. चाहे तो **Date Range** भी डाल सकते हैं (From - To)
3. **Search दबाएं**

### Ledger Format:
| Date | Type | Ref No | Debit | Credit | Balance |
|------|------|--------|-------|--------|---------|

- **Invoice = Debit** (party पर उधार चढ़ा)
- **Payment = Credit** (party से पैसा मिला)
- **Balance = Running Balance** (हर entry के बाद का बकाया)

### Opening & Closing Balance:
- **Opening Balance** = पुराना बकाया + Party का Opening Balance
- **Closing Balance** = Opening + सारे Invoices - सारे Payments

### Ledger PDF / Excel Download:
- **PDF बटन** – पूरा ledger PDF में डाउनलोड करें
- **Excel बटन** – पूरा ledger Excel में डाउनलोड करें

---

## 📋 6. Combined Ledger (सभी Parties का हिसाब)

**Sidebar में "Combined Ledger" पर क्लिक करें.**

यहाँ सभी parties का एक साथ summary दिखेगा:
- Opening Balance
- Total Invoices (कुल बिल)
- Total Payments (कुल भुगतान)
- Closing Balance
- **Outstanding** (बकाया रकम)

---

## ⚙️ 7. Settings (सेटिंग्स)

**Sidebar में "Settings" पर क्लिक करें.**

### Business Settings:
- **Business Name** – आपके व्यवसाय का नाम (जो PDF पर छपेगा)
- **Address, Mobile, Email** – PDF पर दिखेंगे
- **Invoice Prefix** – जैसे `INV-` तो invoice number `INV-00001` बनेगा
- **Payment Prefix** – जैसे `PAY-` तो payment number `PAY-00001` बनेगा

### Change Password:
- पुराना password डालकर नया password सेट करें

---

## 🔢 8. Outstanding Calculation (बकाया कैलकुलेशन)

```
Outstanding = Opening Balance + Total Invoices - Total Payments
```

**Example:**
- Opening Balance = ₹5,000 (party आपको देती है)
- Total Invoices = ₹10,000 (आपने और बिल बनाए)
- Total Payments = ₹3,000 (party ने पैसे दिए)
- **Outstanding = 5,000 + 10,000 - 3,000 = ₹12,000**

**Positive Outstanding** = Party आपको पैसे देती है (लाल रंग में)
**Negative Outstanding** = आप party को पैसे देते हैं (हरे रंग में)

---

## ❓ 9. Common Questions

**Q: अगर गलती से गलत Party डिलीट कर दी?**
A: Database backup न हो तो डेटा वापस नहीं आ सकता। Delete करते वक्त confirmation आती है, ध्यान से पढ़ें।

**Q: Tax क्यों नहीं है?**
A: यह सिस्टम बिना Tax के billing के लिए बना है। अगर Tax चाहिए तो अलग से develop करना होगा।

**Q: PDF क्यों नहीं खुल रही?**
A: ReportLab लाइब्रेरी install होनी चाहिए। `pip install reportlab` चलाएं।

**Q: Excel क्यों नहीं डाउनलोड हो रहा?**
A: openpyxl install होना चाहिए। `pip install openpyxl` चलाएं।

**Q: Outstanding सही नहीं दिख रहा?**
A: सारे Invoices और Payments check करें। Date range filter लगा हो सकता है।

---

## 🚀 10. Quick Workflow (रोज़ का काम)

```
1. Login करें (admin / 1234)
2. नया Party जोड़ें (Parties → Add Party)
3. नया Invoice बनाएं (Invoices → New Invoice)
4. जब payment मिले तो दर्ज करें (Payments → Record Payment)
5. लेखा देखें (Ledger → Party Select → Search)
6. महीने के अंत में PDF/Excel डाउनलोड करें
```

---

> **Need Help?** अपने सिस्टम एडमिन से संपर्क करें।
