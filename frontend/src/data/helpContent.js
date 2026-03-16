export const helpContent = {
  dashboard: {
    en: {
      title: "War Room Guide",
      steps: [
        "Green Light: All compliant. Yellow: Warning. Red: Critical Action Required.",
        "Revenue Pulse: Shows collected vs pending rent for THIS month.",
        "Issue Inbox: Manage repair tickets here.",
        "Daily Closing: Reconcile cash at 10 PM daily."
      ]
    },
    ur: {
      title: "War Room Hidayat",
      steps: [
        "Sabz: Sab theek. Peela: Warning. Laal: Foran Action Lain.",
        "Aamdani: Iss mahinay ka jama shuda aur baqi kiraya.",
        "Shikayat Box: Yahan marammat ke maslay hal karain.",
        "Rozana Closing: Raat 10 baje cash ka hisab karain."
      ]
    }
  },
  compliance: {
    en: {
      title: "Compliance Logic",
      steps: [
        "Normal (0-7 Days): New tenant grace period.",
        "Warning (8-30 Days): Document follow-up needed.",
        "Critical (30+ Days): Police verification mandatory. Alert Owner."
      ]
    },
    ur: {
      title: "Qanooni Hidayat",
      steps: [
        "Normal (0-7 Din): Naye kirayedar ka time.",
        "Warning (8-30 Din): Kaghzat ka pata karain.",
        "Critical (30+ Din): Police verification lazmi hai. Malik ko batain."
      ]
    }
  },
  closing: {
    en: {
      title: "Daily Closing Steps",
      steps: [
        "1. Enter Opening Balance (Cash from yesterday).",
        "2. Add Today's Collections (Rent + Deposit).",
        "3. Subtract Cash Expenses (Repairs/ Bills).",
        "4. Verify 'Cash in Hand' matches your drawer."
      ]
    },
    ur: {
      title: "Rozana Closing Ka Tareeqa",
      steps: [
        "1. Opening Balance likhain (Kal ka bacha hua cash).",
        "2. Aaj ki wasooli shamil karain (Kiraya + Deposit).",
        "3. Kharchay manfi karain (Marammat/Bill).",
        "4. 'Cash in Hand' ko apne drawer se milain."
      ]
    }
  }
};
