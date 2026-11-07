# PRB Research Manager — v1.4 daily work and research release

**This is the existing local-first PRB web app, extended in place.** The app keeps its established browser storage key (`prb-research-manager-v1`) and existing R00 person/source IDs, project records, timesheet entries, imported Drive links, and previous features. It does not use a second task database.

## New views and workflows
- To-Do directly below Dashboard: Today, Overdue, Missed follow-ups, Waiting On, Upcoming, Recurring, Completed, Unscheduled. Every To-Do action edits `tasks` used by the full Tasks table and Dashboard.
- Today's To-Do dashboard: due today, overdue, missed follow-ups, waiting replies, deadlines, next project action, and active timer.
- Quick Capture: task, question, lead, person, source, website, document, or uncategorized Inbox item. Items can be triaged into existing record collections.
- Research section: linked Questions, detailed Research Logs including negative findings and search coverage, active Session workspace, follow-ups, bookmarks, and Inbox.
- Research session: uses the existing timer and Timesheet, preserves task/question links, records findings/source gaps/next action, and can create one linked next-action task.
- Contact follow-up details and parent/child task tracking. Recurring tasks generate one future occurrence after completion and keep the prior record.
- Drive Library: searchable private-file links plus Document Inbox, citation, people/source/task associations, review status, duplicate candidate detection, and non-destructive intake.
- Reference: six planning templates; saved research bookmarks.
- Visuals: family, FAN, timeline, households, evidence, migration, source workflow flowchart, ownership chain, and linked document/person/source network. Graph nodes open their records.
- Finances: expense table, project-level hours, invoice ledger, paid totals, and profitability only where separate internal labor-cost inputs exist.
- Existing optional November 7 legacy-timesheet archive, saved activity timestamps, and source-code workflow are preserved.

## Privacy and local storage
No automatic Google Drive synchronization and **no private genealogy records in this public web-app package**. Records and imported Drive metadata stay in the device browser's local storage, and local source attachments stay in IndexedDB. Browser clearing may erase them. Use **Settings → Export full backup** before clearing data or moving devices. Do not use this unauthenticated app as confidential client-data storage.

## Browser acceptance testing
Tested in Chromium using actual interactive form flows: navigation desktop/mobile; existing JSON import twice without duplicate IDs; due and missed follow-ups; same-record task completion; recurring next task; parent-linked follow-up; Question and negative research log; timer-linked session with next action; source/document intake; ownership visual; claim graph click-through; invoice; reference template; full backup; reload; legacy archive and source workflow visual. No page runtime errors in these tests. Live device-specific behavior still needs user verification.

Deployment requires serving this folder over HTTPS. The service worker uses version `prb-research-v1.4.0` to clear its earlier cache.

Preserves concurrent live additions: person-category source identifiers (e.g., 004o1), source-status legend beneath the timer, network-first app-shell updates, legacy session archiving, and source workflow diagram.