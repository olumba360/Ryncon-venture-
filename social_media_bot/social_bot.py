#!/usr/bin/env python3
"""
Social Media Management Bot - Compliant Version
Features: Rate limiting, consent-based messaging, analytics
Platforms: Telegram, Facebook, Instagram

IMPORTANT: This bot requires explicit consent from group admins
and respects platform rate limits to avoid bans.
"""

import json
import time
import random
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('social_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MessageCampaign:
    """Represents a messaging campaign with compliance checks"""
    id: str
    platform: str
    target_groups: List[str]
    message_template: str
    schedule_time: Optional[datetime]
    rate_limit_seconds: int = 60  # Minimum seconds between messages
    daily_limit: int = 50  # Maximum messages per day
    status: str = "pending"
    created_at: datetime = None
    sent_count: int = 0
    failed_count: int = 0

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def to_dict(self):
        return asdict(self)

class RateLimiter:
    """Ensures compliance with platform rate limits"""

    def __init__(self):
        self.last_message_time = {}
        self.daily_counts = {}
        self.reset_daily_counts()

    def reset_daily_counts(self):
        """Reset daily message counts at midnight"""
        today = datetime.now().date()
        self.daily_counts = {today: {}}

    def can_send(self, platform: str, campaign_id: str, rate_limit: int, daily_limit: int) -> bool:
        """Check if message can be sent within rate limits"""
        now = time.time()
        today = datetime.now().date()

        # Check daily limit
        platform_count = self.daily_counts.get(today, {}).get(platform, 0)
        if platform_count >= daily_limit:
            logger.warning(f"Daily limit reached for {platform}")
            return False

        # Check rate limit
        last_sent = self.last_message_time.get(f"{platform}_{campaign_id}", 0)
        if now - last_sent < rate_limit:
            wait_time = rate_limit - (now - last_sent)
            logger.info(f"Rate limit active. Wait {wait_time:.0f} seconds")
            return False

        return True

    def record_send(self, platform: str, campaign_id: str):
        """Record a successful message send"""
        now = time.time()
        today = datetime.now().date()

        self.last_message_time[f"{platform}_{campaign_id}"] = now

        if today not in self.daily_counts:
            self.daily_counts[today] = {}
        self.daily_counts[today][platform] = self.daily_counts[today].get(platform, 0) + 1

class ComplianceManager:
    """Manages compliance with platform Terms of Service"""

    PROHIBITED_KEYWORDS = [
        "spam", "scam", "fake", "click here", "act now",
        "limited time", "urgent", "winner", "prize"
    ]

    def __init__(self):
        self.approved_groups_file = "approved_groups.json"
        self.load_approved_groups()

    def load_approved_groups(self):
        """Load list of groups where admin consent has been obtained"""
        if Path(self.approved_groups_file).exists():
            with open(self.approved_groups_file, 'r') as f:
                self.approved_groups = json.load(f)
        else:
            self.approved_groups = {}

    def save_approved_groups(self):
        """Save approved groups list"""
        with open(self.approved_groups_file, 'w') as f:
            json.dump(self.approved_groups, f, indent=2)

    def add_approved_group(self, platform: str, group_id: str, admin_contact: str):
        """Add a group with verified admin consent"""
        if platform not in self.approved_groups:
            self.approved_groups[platform] = {}

        self.approved_groups[platform][group_id] = {
            "approved_at": datetime.now().isoformat(),
            "admin_contact": admin_contact,
            "active": True
        }
        self.save_approved_groups()
        logger.info(f"Added approved group: {platform}/{group_id}")

    def is_group_approved(self, platform: str, group_id: str) -> bool:
        """Check if group has admin approval"""
        return (
            platform in self.approved_groups and
            group_id in self.approved_groups[platform] and
            self.approved_groups[platform][group_id].get("active", False)
        )

    def validate_message(self, message: str) -> tuple[bool, str]:
        """Validate message content for compliance"""
        message_lower = message.lower()

        # Check for prohibited keywords
        for keyword in self.PROHIBITED_KEYWORDS:
            if keyword in message_lower:
                return False, f"Message contains prohibited keyword: {keyword}"

        # Check message length
        if len(message) > 1000:
            return False, "Message exceeds 1000 character limit"

        # Check for excessive capitalization
        caps_ratio = sum(1 for c in message if c.isupper()) / max(len(message), 1)
        if caps_ratio > 0.5:
            return False, "Message contains excessive capitalization"

        return True, "Message validated"

class SocialMediaBot:
    """Main bot class with compliance features"""

    def __init__(self):
        self.rate_limiter = RateLimiter()
        self.compliance = ComplianceManager()
        self.campaigns = []
        self.running = False
        self.load_campaigns()

        # Target group categories
        self.target_categories = {
            "tech": ["programming", "web development", "coding", "software"],
            "trading": ["crypto", "forex", "trading", "investment", "stocks"],
            "bots": ["automation", "telegram bots", "discord bots", "whatsapp api"]
        }

    def load_campaigns(self):
        """Load saved campaigns"""
        if Path("campaigns.json").exists():
            with open("campaigns.json", 'r') as f:
                data = json.load(f)
                self.campaigns = [MessageCampaign(**c) for c in data]

    def save_campaigns(self):
        """Save campaigns to file"""
        with open("campaigns.json", 'w') as f:
            json.dump([c.to_dict() for c in self.campaigns], f, indent=2, default=str)

    def create_campaign(self,
                       platform: str,
                       target_groups: List[str],
                       message: str,
                       schedule: Optional[datetime] = None,
                       rate_limit: int = 60,
                       daily_limit: int = 50) -> tuple[bool, str]:
        """Create a new messaging campaign"""

        # Validate message
        is_valid, msg = self.compliance.validate_message(message)
        if not is_valid:
            return False, msg

        # Validate targets
        valid_targets = []
        for group in target_groups:
            if self.compliance.is_group_approved(platform, group):
                valid_targets.append(group)
            else:
                logger.warning(f"Group {group} not approved. Skipping.")

        if not valid_targets:
            return False, "No approved target groups found"

        # Create campaign
        campaign_id = f"{platform}_{int(time.time())}"
        campaign = MessageCampaign(
            id=campaign_id,
            platform=platform,
            target_groups=valid_targets,
            message_template=message,
            schedule_time=schedule,
            rate_limit_seconds=rate_limit,
            daily_limit=daily_limit
        )

        self.campaigns.append(campaign)
        self.save_campaigns()

        logger.info(f"Campaign created: {campaign_id}")
        return True, f"Campaign created with ID: {campaign_id}"

    def execute_campaign(self, campaign_id: str) -> dict:
        """Execute a campaign with full compliance checks"""
        campaign = next((c for c in self.campaigns if c.id == campaign_id), None)
        if not campaign:
            return {"error": "Campaign not found"}

        if campaign.status == "completed":
            return {"error": "Campaign already completed"}

        results = {
            "campaign_id": campaign_id,
            "started_at": datetime.now().isoformat(),
            "sent": [],
            "failed": [],
            "skipped": []
        }

        campaign.status = "running"

        for group in campaign.target_groups:
            # Check rate limits
            if not self.rate_limiter.can_send(
                campaign.platform,
                campaign.id,
                campaign.rate_limit_seconds,
                campaign.daily_limit
            ):
                results["skipped"].append({
                    "group": group,
                    "reason": "Rate limit exceeded"
                })
                continue

            # Simulate sending (replace with actual API calls)
            try:
                success = self._send_message(
                    campaign.platform,
                    group,
                    campaign.message_template
                )

                if success:
                    self.rate_limiter.record_send(campaign.platform, campaign.id)
                    campaign.sent_count += 1
                    results["sent"].append({"group": group, "time": datetime.now().isoformat()})
                    logger.info(f"Message sent to {group}")
                else:
                    campaign.failed_count += 1
                    results["failed"].append({"group": group, "reason": "Send failed"})

                # Rate limit delay
                time.sleep(random.uniform(campaign.rate_limit_seconds, campaign.rate_limit_seconds + 10))

            except Exception as e:
                logger.error(f"Error sending to {group}: {e}")
                results["failed"].append({"group": group, "reason": str(e)})

        campaign.status = "completed" if campaign.failed_count == 0 else "partial"
        self.save_campaigns()

        results["completed_at"] = datetime.now().isoformat()
        results["total_sent"] = campaign.sent_count
        results["total_failed"] = campaign.failed_count

        return results

    def _send_message(self, platform: str, target: str, message: str) -> bool:
        """
        Send message to target platform.
        This is a simulation - implement actual API calls here.
        """
        # TODO: Implement actual API calls
        # For Telegram: python-telegram-bot
        # For Facebook: facebook-sdk
        # For Instagram: instagrapi

        logger.info(f"[SIMULATION] Sending to {platform}/{target}")
        time.sleep(0.5)  # Simulate network delay
        return True

    def get_analytics(self) -> dict:
        """Get campaign analytics"""
        total_sent = sum(c.sent_count for c in self.campaigns)
        total_failed = sum(c.failed_count for c in self.campaigns)

        return {
            "total_campaigns": len(self.campaigns),
            "total_sent": total_sent,
            "total_failed": total_failed,
            "success_rate": (total_sent / max(total_sent + total_failed, 1)) * 100,
            "platforms": list(set(c.platform for c in self.campaigns)),
            "daily_stats": self.rate_limiter.daily_counts
        }

    def run_scheduler(self):
        """Background scheduler for campaigns"""
        while self.running:
            now = datetime.now()

            for campaign in self.campaigns:
                if (
                    campaign.status == "pending" and
                    campaign.schedule_time and
                    campaign.schedule_time <= now
                ):
                    logger.info(f"Auto-executing scheduled campaign: {campaign.id}")
                    self.execute_campaign(campaign.id)

            time.sleep(60)  # Check every minute

    def start(self):
        """Start the bot scheduler"""
        self.running = True
        scheduler_thread = threading.Thread(target=self.run_scheduler, daemon=True)
        scheduler_thread.start()
        logger.info("Bot scheduler started")

    def stop(self):
        """Stop the bot scheduler"""
        self.running = False
        logger.info("Bot scheduler stopped")

# Example usage and CLI interface
if __name__ == "__main__":
    bot = SocialMediaBot()

    print("=" * 50)
    print("Social Media Management Bot - Compliant Version")
    print("=" * 50)
    print("\nThis bot requires explicit admin consent for all groups.")
    print("Rate limiting and daily limits are enforced automatically.\n")

    while True:
        print("\nCommands:")
        print("1. Add approved group")
        print("2. Create campaign")
        print("3. Execute campaign")
        print("4. View analytics")
        print("5. List campaigns")
        print("6. Start scheduler")
        print("7. Exit")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            platform = input("Platform (telegram/facebook/instagram): ").strip()
            group_id = input("Group ID/URL: ").strip()
            admin = input("Admin contact (for verification): ").strip()
            bot.compliance.add_approved_group(platform, group_id, admin)
            print(f"✓ Group {group_id} approved")

        elif choice == "2":
            platform = input("Platform: ").strip()
            groups = input("Target groups (comma-separated): ").strip().split(",")
            groups = [g.strip() for g in groups]
            message = input("Message: ").strip()
            rate_limit = int(input("Rate limit (seconds, min 60): ") or "60")
            daily_limit = int(input("Daily limit (max 50): ") or "50")

            success, msg = bot.create_campaign(
                platform=platform,
                target_groups=groups,
                message=message,
                rate_limit=max(rate_limit, 60),
                daily_limit=min(daily_limit, 50)
            )
            print(f"{'✓' if success else '✗'} {msg}")

        elif choice == "3":
            campaign_id = input("Campaign ID: ").strip()
            results = bot.execute_campaign(campaign_id)
            print(json.dumps(results, indent=2, default=str))

        elif choice == "4":
            analytics = bot.get_analytics()
            print(json.dumps(analytics, indent=2, default=str))

        elif choice == "5":
            for c in bot.campaigns:
                print(f"\nID: {c.id}")
                print(f"  Platform: {c.platform}")
                print(f"  Status: {c.status}")
                print(f"  Sent: {c.sent_count}, Failed: {c.failed_count}")

        elif choice == "6":
            bot.start()
            print("✓ Scheduler started in background")

        elif choice == "7":
            bot.stop()
            print("Goodbye!")
            break
