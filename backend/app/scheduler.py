import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.services.attendance_service import trigger_absentee_cutoff_job
from app.config import settings

logger = logging.getLogger("attendance.scheduler")

scheduler = AsyncIOScheduler()

def run_daily_9am_absentee_job():
    """
    Scheduled task callback executing daily at 9:00 AM.
    Identifies all registered users who haven't scanned in and marks them as ABSENT.
    """
    logger.info("CRON TRIGGER: Starting 9:00 AM Automated Absentee Cutoff Job...")
    try:
        result = trigger_absentee_cutoff_job()
        logger.info(f"CRON SUCCESS: {result['message']} - Marked {result['absent_count']} users as ABSENT.")
    except Exception as e:
        logger.error(f"CRON ERROR: 9:00 AM Cutoff Job failed with exception: {e}")

def start_scheduler():
    """Starts the APScheduler background daemon."""
    cutoff_parts = settings.CUTOFF_TIME.split(":")
    hour = int(cutoff_parts[0])
    minute = int(cutoff_parts[1])
    
    # Configure daily cron trigger at CUTOFF_TIME (default 09:00 AM)
    trigger = CronTrigger(hour=hour, minute=minute)
    scheduler.add_job(
        run_daily_9am_absentee_job,
        trigger=trigger,
        id="daily_absentee_cutoff_job",
        replace_existing=True,
        name="Daily 9:00 AM Absentee Attendance Processing"
    )
    
    scheduler.start()
    logger.info(f"APScheduler daemon started successfully. Scheduled daily job for {settings.CUTOFF_TIME} AM.")

def stop_scheduler():
    """Shuts down the background scheduler."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler daemon shut down.")
