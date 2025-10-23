"""
Emergency Escalation System for SeniorSafe AI
Detects urgent situations and provides immediate action guidance.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class UrgencyLevel(Enum):
    """Urgency levels for different situations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class EmergencyResponse:
    """Represents an emergency response with urgency level and actions"""
    urgency_level: UrgencyLevel
    title: str
    immediate_actions: List[str]
    explanation: str
    emergency_contacts: List[Dict[str, str]]
    follow_up_actions: Optional[List[str]] = None


class UrgencyDetector:
    """Detects urgency level in user messages"""

    # Critical urgency keywords - immediate threat or active crime
    CRITICAL_KEYWORDS = [
        'right now', 'happening now', 'currently', 'at this moment',
        'they are', 'he is', 'she is', 'someone is',
        'locked out', 'cant access', "can't access", 'frozen account',
        'threatening', 'demanding', 'on the phone with',
        'remote access', 'on my computer', 'controlling my',
        'just gave', 'just sent', 'just transferred',
        'wire transfer', 'sending money now', 'about to send'
    ]

    # High urgency keywords - recent incident requiring fast action
    HIGH_URGENCY_KEYWORDS = [
        'just happened', 'just received', 'just got',
        'today', 'this morning', 'this afternoon', 'tonight',
        'few minutes ago', 'hour ago', 'hours ago',
        'unauthorized', 'suspicious transaction', 'strange charge',
        'dont recognize', "don't recognize", 'didnt authorize', "didn't authorize",
        'compromised', 'hacked', 'breached', 'stolen',
        'gave them', 'shared my', 'told them my',
        'clicked', 'downloaded', 'installed',
        'social security number', 'ssn', 'credit card', 'bank account'
    ]

    # Medium urgency keywords - concern but not immediate
    MEDIUM_URGENCY_KEYWORDS = [
        'yesterday', 'last night', 'few days ago',
        'suspicious', 'worried', 'concerned', 'afraid',
        'might have', 'may have', 'think i', 'not sure if',
        'received email', 'got call', 'voicemail',
        'asking for', 'requesting', 'wants me to'
    ]

    # Critical scenarios - specific situations requiring immediate action
    CRITICAL_SCENARIOS = {
        'active_bank_fraud': [
            'unauthorized transfer', 'money leaving', 'funds transferred',
            'someone withdrew', 'suspicious withdrawal', 'account drained'
        ],
        'device_compromised': [
            'remote access', 'controlling my computer', 'screen sharing',
            'teamviewer', 'anydesk', 'remote desktop', 'cant control',
            "can't control"
        ],
        'personal_threat': [
            'threatening', 'blackmail', 'extortion', 'will hurt',
            'sending police', 'arrest warrant', 'immediate legal action'
        ],
        'active_scam_call': [
            'on the phone', 'caller is', 'they are saying',
            'asking me to', 'telling me to', 'wants me to go'
        ],
        'payment_in_progress': [
            'about to send', 'about to pay', 'ready to transfer',
            'gift cards', 'wire transfer', 'cryptocurrency', 'bitcoin'
        ]
    }

    @classmethod
    def detect_urgency(cls, message: str) -> Tuple[UrgencyLevel, Optional[str]]:
        """
        Detect urgency level from message content
        Returns: (UrgencyLevel, scenario_type or None)
        """
        message_lower = message.lower()

        # Check for critical scenarios first
        for scenario, keywords in cls.CRITICAL_SCENARIOS.items():
            if any(keyword in message_lower for keyword in keywords):
                return (UrgencyLevel.CRITICAL, scenario)

        # Check for critical keywords
        if any(keyword in message_lower for keyword in cls.CRITICAL_KEYWORDS):
            return (UrgencyLevel.CRITICAL, 'general_critical')

        # Check for high urgency keywords
        if any(keyword in message_lower for keyword in cls.HIGH_URGENCY_KEYWORDS):
            return (UrgencyLevel.HIGH, 'recent_incident')

        # Check for medium urgency keywords
        if any(keyword in message_lower for keyword in cls.MEDIUM_URGENCY_KEYWORDS):
            return (UrgencyLevel.MEDIUM, 'general_concern')

        # Default to low urgency
        return (UrgencyLevel.LOW, None)


class EmergencyResponseGenerator:
    """Generates appropriate emergency responses based on urgency level and scenario"""

    EMERGENCY_RESPONSES = {
        'active_bank_fraud': EmergencyResponse(
            urgency_level=UrgencyLevel.CRITICAL,
            title="🚨 URGENT: Active Bank Fraud Detected",
            immediate_actions=[
                "**CALL YOUR BANK IMMEDIATELY** - Use the number on the back of your card or bank statement",
                "**Report unauthorized transactions** - Tell them you're experiencing fraud RIGHT NOW",
                "**Ask them to FREEZE your account** - Prevent further unauthorized transactions",
                "**Do NOT hang up** until your account is secured",
                "**Do NOT make any transfers or payments** that anyone is asking you to make",
                "**If someone is with you or on the phone**, hang up on them immediately"
            ],
            explanation=(
                "Active bank fraud requires IMMEDIATE action. Every minute counts. "
                "Your bank has 24/7 fraud departments specifically for this situation."
            ),
            emergency_contacts=[
                {
                    'name': 'Your Bank',
                    'action': 'Call the number on your card NOW',
                    'priority': 'HIGHEST'
                },
                {
                    'name': 'Local Police (Emergency)',
                    'phone': '911',
                    'action': 'If you feel threatened or in danger',
                    'priority': 'CRITICAL'
                }
            ],
            follow_up_actions=[
                "File a police report",
                "Contact credit bureaus to place fraud alert",
                "Change all banking passwords",
                "Request new cards/account numbers",
                "Monitor accounts daily"
            ]
        ),

        'device_compromised': EmergencyResponse(
            urgency_level=UrgencyLevel.CRITICAL,
            title="🚨 URGENT: Device Compromised - Immediate Action Required",
            immediate_actions=[
                "**DISCONNECT FROM INTERNET IMMEDIATELY** - Unplug ethernet cable or turn off Wi-Fi",
                "**SHUT DOWN your computer** - Hold power button until it turns off",
                "**DO NOT turn it back on yet**",
                "**If someone is remotely controlling it**, they can see everything you do",
                "**Change passwords from a DIFFERENT device** - Phone or tablet",
                "**Call your bank from a different device** - Report possible compromise"
            ],
            explanation=(
                "If someone has remote access to your computer, they can see your passwords, "
                "banking information, and personal files RIGHT NOW. Disconnecting immediately "
                "stops them from causing more damage."
            ),
            emergency_contacts=[
                {
                    'name': 'Your Bank',
                    'action': 'Call from a different device to secure accounts',
                    'priority': 'HIGHEST'
                },
                {
                    'name': 'Local Computer Repair',
                    'action': 'Find a trusted technician to clean your computer',
                    'priority': 'HIGH'
                }
            ],
            follow_up_actions=[
                "Have computer professionally cleaned/reimaged",
                "Install legitimate antivirus software",
                "Change ALL passwords from a clean device",
                "Monitor bank and credit card statements",
                "Enable two-factor authentication everywhere"
            ]
        ),

        'active_scam_call': EmergencyResponse(
            urgency_level=UrgencyLevel.CRITICAL,
            title="🚨 URGENT: You May Be on the Phone with a Scammer RIGHT NOW",
            immediate_actions=[
                "**HANG UP THE PHONE IMMEDIATELY** - Do not continue the conversation",
                "**DO NOT call them back** - The number is fake",
                "**DO NOT do what they asked** - No payments, no downloads, no information",
                "**Block the number** on your phone",
                "**If they call back, DO NOT ANSWER**",
                "**Take a deep breath** - You did the right thing by hanging up"
            ],
            explanation=(
                "Scammers use pressure tactics to keep you on the phone. The longer you stay "
                "on the call, the more likely they are to succeed. Hanging up is ALWAYS the "
                "right choice, even if they claim to be from the government, police, or your bank."
            ),
            emergency_contacts=[
                {
                    'name': 'Real Organization',
                    'action': 'Look up the official number yourself and call to verify',
                    'priority': 'HIGH'
                },
                {
                    'name': 'Local Police (Non-Emergency)',
                    'action': 'Report the scam call',
                    'priority': 'MEDIUM'
                }
            ],
            follow_up_actions=[
                "Report to Federal Trade Commission (FTC) at reportfraud.ftc.gov",
                "Tell family/friends about the scam",
                "Consider call-blocking apps",
                "Register on Do Not Call Registry"
            ]
        ),

        'payment_in_progress': EmergencyResponse(
            urgency_level=UrgencyLevel.CRITICAL,
            title="🚨 STOP: Do NOT Make This Payment",
            immediate_actions=[
                "**STOP IMMEDIATELY** - Do not complete the payment",
                "**Gift cards are for SCAMS** - Legitimate businesses never ask for gift cards",
                "**Wire transfers cannot be reversed** - Once sent, money is gone forever",
                "**Cryptocurrency is untraceable** - You will never get it back",
                "**Hang up** if someone is pressuring you",
                "**Call the organization directly** - Use a number you look up yourself"
            ],
            explanation=(
                "Scammers create urgency and pressure to make you send money quickly. "
                "NO legitimate government agency, tech company, or business will EVER ask you to: "
                "pay with gift cards, wire transfer money, or send cryptocurrency. These are ALWAYS scams."
            ),
            emergency_contacts=[
                {
                    'name': 'Trusted Family/Friend',
                    'action': 'Talk to someone you trust before sending any money',
                    'priority': 'HIGHEST'
                },
                {
                    'name': 'Organization You Are Supposedly Paying',
                    'action': 'Call their REAL number from their official website',
                    'priority': 'HIGH'
                }
            ],
            follow_up_actions=[
                "Report to FTC at reportfraud.ftc.gov",
                "Report to IC3.gov if internet-related",
                "Tell family members about this scam attempt",
                "Learn warning signs of payment scams"
            ]
        ),

        'personal_threat': EmergencyResponse(
            urgency_level=UrgencyLevel.CRITICAL,
            title="🚨 URGENT: Threats Require Immediate Police Contact",
            immediate_actions=[
                "**CALL 911 if you feel in immediate danger**",
                "**Document everything** - Save messages, emails, voicemails, caller IDs",
                "**DO NOT engage with the threatener** - Do not respond to threats",
                "**Tell someone you trust** - Family member, friend, or neighbor",
                "**File a police report** - Even if you don't feel in immediate danger",
                "**These threats are likely fake** - Scammers use fear to control you"
            ],
            explanation=(
                "Scammers often use threats of arrest, lawsuits, or harm to create panic. "
                "Real law enforcement will NEVER call to threaten you over the phone. "
                "Real courts send official letters, not phone calls. But threats should still "
                "be reported to actual police."
            ),
            emergency_contacts=[
                {
                    'name': 'Emergency Services',
                    'phone': '911',
                    'action': 'Call immediately if you feel threatened or in danger',
                    'priority': 'CRITICAL'
                },
                {
                    'name': 'Local Police (Non-Emergency)',
                    'action': 'File a report about the threatening calls/messages',
                    'priority': 'HIGH'
                }
            ],
            follow_up_actions=[
                "Keep detailed log of all threats",
                "Consider restraining order if threats continue",
                "Block threatening numbers/emails",
                "Report to FBI at ic3.gov",
                "Notify family members"
            ]
        ),

        'recent_incident': EmergencyResponse(
            urgency_level=UrgencyLevel.HIGH,
            title="⚠️ IMPORTANT: Take Action Within 24 Hours",
            immediate_actions=[
                "**Act quickly** - The sooner you act, the better your chances of minimizing damage",
                "**Call your bank** - Report any financial information you shared",
                "**Change passwords** - For any accounts that may be compromised",
                "**Run antivirus scan** - If you downloaded anything or visited suspicious sites",
                "**Document everything** - Save emails, messages, caller IDs, screenshots",
                "**Don't panic** - You're taking the right steps by seeking help"
            ],
            explanation=(
                "Recent incidents require prompt action but you have time to be thorough. "
                "Taking these steps within 24 hours significantly reduces potential damage."
            ),
            emergency_contacts=[
                {
                    'name': 'Your Bank/Credit Card',
                    'action': 'Report if you shared financial information',
                    'priority': 'HIGH'
                },
                {
                    'name': 'FTC at reportfraud.ftc.gov',
                    'action': 'File an official report',
                    'priority': 'MEDIUM'
                }
            ],
            follow_up_actions=[
                "Monitor bank and credit card statements",
                "Consider credit monitoring service",
                "Place fraud alert on credit reports",
                "Report to appropriate authorities",
                "Learn about this type of scam"
            ]
        )
    }

    @classmethod
    def generate_response(cls, urgency_level: UrgencyLevel, scenario: Optional[str]) -> EmergencyResponse:
        """Generate appropriate response based on urgency level and scenario"""

        # If we have a specific scenario, use that response
        if scenario and scenario in cls.EMERGENCY_RESPONSES:
            return cls.EMERGENCY_RESPONSES[scenario]

        # Otherwise, use general critical response
        if urgency_level == UrgencyLevel.CRITICAL:
            return EmergencyResponse(
                urgency_level=UrgencyLevel.CRITICAL,
                title="🚨 URGENT: Immediate Action Required",
                immediate_actions=[
                    "**STOP what you are doing** - Do not proceed with any payments or downloads",
                    "**Hang up** if someone is on the phone pressuring you",
                    "**Disconnect** if someone has remote access to your computer",
                    "**Call your bank** if you shared financial information",
                    "**Contact local police** if you feel threatened",
                    "**Take a breath** - You're doing the right thing by seeking help"
                ],
                explanation=(
                    "This situation requires immediate action to prevent or minimize damage. "
                    "Follow the steps above right now, then we can help with next steps."
                ),
                emergency_contacts=[
                    {
                        'name': 'Emergency Services',
                        'phone': '911',
                        'action': 'If you are in immediate danger',
                        'priority': 'CRITICAL'
                    },
                    {
                        'name': 'Your Bank',
                        'action': 'If financial accounts are at risk',
                        'priority': 'HIGH'
                    }
                ]
            )

        elif urgency_level == UrgencyLevel.HIGH:
            return cls.EMERGENCY_RESPONSES['recent_incident']

        # For medium/low urgency, return None to use normal response
        return None


class EmergencyResponseFormatter:
    """Formats emergency responses for display"""

    @staticmethod
    def format_response(response: EmergencyResponse) -> str:
        """Format emergency response as markdown with visual prominence"""

        output = f"# {response.title}\n\n"
        output += "---\n\n"

        # Explanation
        output += f"**{response.explanation}**\n\n"
        output += "---\n\n"

        # Immediate actions
        output += "## 🔴 DO THIS RIGHT NOW:\n\n"
        for i, action in enumerate(response.immediate_actions, 1):
            output += f"{i}. {action}\n\n"

        # Emergency contacts
        if response.emergency_contacts:
            output += "---\n\n"
            output += "## 📞 Emergency Contacts:\n\n"
            for contact in response.emergency_contacts:
                output += f"**{contact['name']}**"
                if 'phone' in contact:
                    output += f" - {contact['phone']}"
                output += "\n"
                output += f"- Priority: {contact['priority']}\n"
                output += f"- Action: {contact['action']}\n\n"

        # Follow-up actions
        if response.follow_up_actions:
            output += "---\n\n"
            output += "## ✅ After Immediate Actions, Do These:\n\n"
            for i, action in enumerate(response.follow_up_actions, 1):
                output += f"{i}. {action}\n"
            output += "\n"

        output += "---\n\n"
        output += "**Once you've taken these immediate steps, I can help you with:**\n"
        output += "- Finding local resources to report this crime\n"
        output += "- Understanding what happened\n"
        output += "- Protecting yourself from future scams\n"
        output += "- Step-by-step recovery process\n\n"
        output += "*Please let me know once you've completed the immediate actions above.*"

        return output


def check_for_emergency(message: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a message indicates an emergency situation
    Returns: (is_emergency, formatted_response or None)
    """
    urgency_level, scenario = UrgencyDetector.detect_urgency(message)

    # Only generate emergency response for HIGH and CRITICAL urgency
    if urgency_level in [UrgencyLevel.HIGH, UrgencyLevel.CRITICAL]:
        response = EmergencyResponseGenerator.generate_response(urgency_level, scenario)
        if response:
            formatted = EmergencyResponseFormatter.format_response(response)
            return (True, formatted)

    return (False, None)


# Example usage and testing
if __name__ == "__main__":
    test_messages = [
        "Someone is on my computer right now with remote access",
        "I just transferred $5000 to someone who called about my taxes",
        "I'm on the phone with someone saying they're from Microsoft",
        "I received a suspicious email yesterday",
        "I think I might have been scammed",
        "Money is being withdrawn from my account right now",
        "They're threatening to arrest me if I don't pay",
        "I'm about to buy $500 in gift cards like they asked"
    ]

    print("Testing Emergency Detection System\n")
    print("=" * 80)

    for message in test_messages:
        print(f"\nMessage: '{message}'")
        print("-" * 80)

        is_emergency, response = check_for_emergency(message)

        if is_emergency:
            print("EMERGENCY DETECTED!")
            print(response[:500] + "...\n")
        else:
            urgency, scenario = UrgencyDetector.detect_urgency(message)
            print(f"Urgency Level: {urgency.value}")
            print(f"Scenario: {scenario if scenario else 'None'}")
            print("Normal response would be used.")

        print("=" * 80)
