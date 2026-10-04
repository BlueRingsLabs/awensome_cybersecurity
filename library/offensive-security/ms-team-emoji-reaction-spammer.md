---
id: ckb-e9e0f752e660
title: MS Team Emoji Reaction Spammer
category: offensive-security
format: article
language: en
tags: [powershell, red-team, soc, tls]
license: NOASSERTION
added: 2026-10-04
classification:
  method: heuristic
  confidence: 0.26
---

# MS Team Emoji Reaction Spammer

I am a pentester and red teamer at work, and an ethical hacker, blogger, gamer and pseudo-developer outside of work. Sometimes I’m a slacker at work too, but I prefer to call it ‘professional’ – meaning I automate my tasks. If there are no red team activities planned for Friday, I don’t do anything myself because, as we all know, Fridays at work are a bit different. Everyone is thinking about the weekend, not the red teamer dumping work or alerts on [SIEM](https://en.wikipedia.org/wiki/Security_information_and_event_management). As a pentester and red teamer, people generally don’t like you, especially when this position is new to the company, because you add to their workload and show in your reports that they are doing their job poorly.

Over time, as awareness of this role grows, you become the best friend of IT people and application developers because you help them to create a secure environment by pointing out where the problem lies and giving tips on how to fix security-related bugs. Everyone is happy with the report, which proves that people are testing what they implement. Over time, when they retest, the report no longer glows red, but contains informational additions that may be worth considering for implementation to improve things further. Then everyone smiles.

Unfortunately, as a Red Teamer, the Blue Team will always dislike you. The Red Team has two objectives: one is Red Team vs. Blue Team, but not as a competition; rather, it is to check what we detect and what we don’t. In other words, it is to test the Blue Team’s response to alerts, or to simulate an attack in order to check whether alerts will appear at all. In other words, it is to check whether the organisation is prepared for this type of threat and whether the detection/response mechanisms will work. The second goal is to perform adversary emulation, which involves providing Blue Team/SOC training in conditions that closely resemble a real attack. It also involves checking whether we can catch and remove an attackers before they can cause any further damage. In general, detection and blocking are failures for the Red Teamer in both tasks. Sometimes these tasks are carried out as planned global actions where certain people are in on the secret, and sometimes only the manager of the offensive security department knows about them. This annoys the Blue Team the most. Of course, there is also purple teaming, where both teams collaborate to enhance detection and response capabilities.

I, and probably many other red teamers, irritate our colleagues at work even more sometimes, but I suppose it’s just my mischievous nature coming out, coming up with all sorts of silly ideas. One of these ideas is annoying my colleagues by spamming them with reactions in Microsoft Teams.

![MS Teams Emoji Reaction Spammer](emojispammer.webp)

Yes, a week ago I discovered by accident that Microsoft had added the ability to react to posts multiple times on Teams channels and chats. I don’t know why they did it, and it’s probably not necessary for most people, at least in a business environment. Discord has this feature too, and sometimes people add more reactions in the form of captions. But I immediately thought: ‘I’ll quickly press it a dozen times and see where the limit is, how fast I can do it to make the sound on my phone or desktop annoying, and whether I can automate it to spam others.’ Yes, I know it’s stupid, and I don’t know who needs it, but I did it.

The best thing is that you can’t turn it off in MS Teams, there is no option to disable multi-reactions or limit the number of them.

You can check this [Microsoft learn platform post](https://learn.microsoft.com/en-us/answers/questions/4377754/microsoft-teams-multiple-emoji-reaction-microsoft). One guy called it a pointless feature there. I disagree! Normally, I would say I wrote **Microsoft Teams Emoji Spammer**, but professionally, we can call it **MS Teams Bring Attention Tool**. Because at the right speed of adding 18 reactions to a post, it makes your phone and computer annoying, almost as if you were an influencer with a million followers reacting to your sweet photos on Instagram.

![Multiple Emoji Reaction](msteam-multiple-emoji-reaction.webp)

Well, I checked it out, and I could use PowerShell and MS Graph for that.

Reactions in Teams are displayed in Microsoft Graph as `setReaction`/`unsetReaction` actions on the `chatMessage` object. In PowerShell, this can be handled by the `Microsoft Graph PowerShell SDK` (ready-made cmdlets such as `Set-Mg*`, `MessageReaction`) or the universal `Invoke-MgGraphRequest`.

Unfortunately, when I started writing the script, it turned out that there are certain requirements, namely access to `Microsoft Graph (delegated)`.

Reactions are not supported in application permissions (daemon without a user). The context of the logged-in user (delegated) is required.

Minimum scopes:

- For channels (Teams): `ChannelMessage.Send`
- For chats (1:1/group): `Chat.ReadWrite` and `ChatMessage.Send`

The administrator must grant `consent` to these scopes. More info on [chatMessage: setReaction](https://learn.microsoft.com/en-us/graph/api/chatmessage-setreaction?view=graph-rest-1.0).

Target identifiers such as `teamId`, `channelId`, `messageId` (and possibly `replyId` for threads), or `chatId` + `messageId` for chats. They can be retrieved with Graph (e.g., `Get-MgTeam`, `Get-MgTeamChannel`, `Get-MgTeamChannelMessage`, `Get-MgChatMessage`). Again more info on [Using Get-MgTeamChannelMessage in Graph PowerShell](https://m365corner.com/m365-powershell/using-get-mgteamchannelmessage-in-graph-powershell.html). You can also find these identifiers by copying links to specific messages - “Copy link to message” - they are included in the URL.

Module: `Microsoft.Graph`/`Microsoft.Graph.Teams` (there are ready-made cmdlets `Set-MgTeamChannelMessageReaction`, `Set-MgChatMessageReaction`, etc.). If necessary, `Invoke-MgGraphRequest` should work too.

Unfortunately, I don’t have the necessary permissions, so it could potentially look like this for channels:

```powershell
# IDs – put your ID
$teamId    = "<TEAM-ID>"
$channelId = "<CHANNEL-ID>"
$messageId = "<MESSAGE-ID>"

# 8 emoji, which you want to send
$emojis = @("👍","❤️","😂","🎉","🔥","👏","🤔","🚀")

foreach ($emoji in $emojis) {
    # Add reaction
    Set-MgTeamChannelMessageReaction `
        -TeamId $teamId `
        -ChannelId $channelId `
        -ChatMessageId $messageId `
        -ReactionType $emoji

    Start-Sleep -Seconds 1   # a short pause to avoid throttling
}
```

REST version

```powershell
foreach ($emoji in $emojis) {
    $uri  = "https://graph.microsoft.com/v1.0/teams/$teamId/channels/$channelId/messages/$messageId/setReaction"
    $body = @{ reactionType = $emoji } | ConvertTo-Json
    Invoke-MgGraphRequest -Method POST -Uri $uri -Body $body
    Start-Sleep -Seconds 1
}
```

for chats

```powershell
# IDs – put your ID
$chatId    = "<CHAT-ID>"
$messageId = "<MESSAGE-ID>"

$emojis = @("👍","❤️","😂","🎉","🔥","👏","🤔","🚀")

foreach ($emoji in $emojis) {
    Set-MgChatMessageReaction `
        -ChatId $chatId `
        -ChatMessageId $messageId `
        -ReactionType $emoji

    Start-Sleep -Seconds 1
}
```

REST version

```powershell
foreach ($emoji in $emojis) {
    $uri  = "https://graph.microsoft.com/v1.0/chats/$chatId/messages/$messageId/setReaction"
    $body = @{ reactionType = $emoji } | ConvertTo-Json
    Invoke-MgGraphRequest -Method POST -Uri $uri -Body $body
    Start-Sleep -Seconds 1
}
```

It’s just a theory at the moment, but you know what? I already have a list of users in the company with these permissions, so you can probably guess what my next Red Team exercise goal will be.

Of course, I couldn’t resist spamming my co-workers. So, what’s the best thing to do in this situation? Good old [AutoHotkey](https://www.autohotkey.com/). Since I can do it fairly quickly by hand, maybe an automated tool can do it for me (remember, I’m lazy and like to automate my work).

So I wrote this code. It’s important not to go too fast, otherwise the sounds won’t have time to start. As with any AutoHotkey script, you need to create a shortcut to interrupt the action. Anyone who has used AutoHotkey at least once knows that every mistake causes random clicking everywhere except where you want it to! There is also no limit to the number of emojis you can use in a chat. I used almost 20 in a test. However, there is a limit of about 14 emojis for channels.

Here is the script with comments to help you understand it better. Feel free to tweak it for your needs. It just press shortcut combination to react automatically to messages. It works for me, but in your environment it may need some additional changes.

Quick instruction:

- Run AutoHotkey script
- Select chat message (click on it)
- `Ctrl+Shift+.` - to execute script
  - `Alt+,` - to stop it in case it does something else
- For Teams Channels messages change parameter `ClickBeforeEach:= false` to `ClickBeforeEach:= true`
- Select Teams message (click on it)
- `Ctrl+Shift+.` - to execute script
  - `Alt+,` - to stop it in case it does something else

And here is the script.

```bash
; AutoHotkey v2 — MS Teams emoji reactions spammer
; Start:  Ctrl+Shift+.   (dot)
; STOP:   Alt+,          (comma)
; Toggle Turbo: Ctrl+Shift+T (disabled by default, if enabled it can be too fast and sound for each emoji wont play.)
; Optional mouse click before each reaction (for channel threads, not needed for chats or group chats)

#Requires AutoHotkey v2.0
#UseHook
#SingleInstance Force
#Warn
ProcessSetPriority "High"

; ===================== CONFIG =====================
repeats             := 18     ; how many reactions to add per run
menuDownCount       := 5      ; DOWN presses to reach "Add reaction" in context menu
tabsBeforeSelect    := 2      ; TAB presses inside reaction UI
emojiDownCount      := 3      ; DOWN presses to highlight target emoji

; Click to refocus the thread/message before each iteration:
ClickBeforeEach     := false   ; set to true for channel threads; false for chats
ClickButton         := "L"    ; left mouse button click
ClickCount          := 1      ; number of clicks (1 = single click)
ClickDelayMs        := 60     ; small wait after click

TurboMode           := false   ; faster timings when true

; Safe timings [ms]
t_afterContext_s    := 280
t_inMenu_s          := 110
t_pickerOpen_s      := 320
t_pickerNav_s       := 110
t_afterChoose_s     := 260

; Turbo timings [ms] — aggressive
t_afterContext_f    := 90
t_inMenu_f          := 25
t_pickerOpen_f      := 120
t_pickerNav_f       := 25
t_afterChoose_f     := 110
; ==================================================

; Performance tweaks
SendMode("Input")
SetKeyDelay(-1)
SetMouseDelay(-1)
SetWinDelay(-1)

; Globals (state machine)
global running := false
global queue := []          
global nextAt := 0 ; A_TickCount threshold for next step
global timings := Map()

ResolveTimings() {
    global TurboMode, timings
    if TurboMode {
        timings["afterContext"] := t_afterContext_f
        timings["inMenu"]       := t_inMenu_f
        timings["pickerOpen"]   := t_pickerOpen_f
        timings["pickerNav"]    := t_pickerNav_f
        timings["afterChoose"]  := t_afterChoose_f
    } else {
        timings["afterContext"] := t_afterContext_s
        timings["inMenu"]       := t_inMenu_s
        timings["pickerOpen"]   := t_pickerOpen_s
        timings["pickerNav"]    := t_pickerNav_s
        timings["afterChoose"]  := t_afterChoose_s
    }
}
ResolveTimings()

; Build one “reaction” sequence
EnqueueOneReaction() {
    global queue, ClickBeforeEach, ClickButton, ClickCount, ClickDelayMs
    global menuDownCount, tabsBeforeSelect, emojiDownCount, timings

    ; (Optional) refocus message by clicking at current mouse position
    if ClickBeforeEach {
        queue.Push({type:"click", btn:ClickButton, cnt:ClickCount})
        queue.Push({type:"sleep", data:ClickDelayMs})
    }

    ; Open context menu
    queue.Push({type:"send",  data:"+{F10}"}) ; Shift+F10
    queue.Push({type:"sleep", data:timings["afterContext"]})

    ; Navigate to "Add reaction"
    Loop menuDownCount {
        queue.Push({type:"send",  data:"{Down}"})
        queue.Push({type:"sleep", data:timings["inMenu"]})
    }
    queue.Push({type:"send",  data:"{Enter}"}) ; open reactions
    queue.Push({type:"sleep", data:timings["pickerOpen"]})

    ; Inside picker: Tab x N, Down x N, Enter
    Loop tabsBeforeSelect {
        queue.Push({type:"send",  data:"{Tab}"})
        queue.Push({type:"sleep", data:timings["pickerNav"]})
    }
    Loop emojiDownCount {
        queue.Push({type:"send",  data:"{Down}"})
        queue.Push({type:"sleep", data:timings["pickerNav"]})
    }
    queue.Push({type:"send",  data:"{Enter}"}) ; apply emoji
    queue.Push({type:"sleep", data:timings["afterChoose"]})
}

BuildRun(n) {
    global queue
    queue := []
    Loop n
        EnqueueOneReaction()
    queue.Push({type:"send", data:"{Esc}"}) ; close any leftover UI
}

; Timer callback (non-blocking execution)
TimerTick(*) {
    global running, queue, nextAt
    if !running {
        SetTimer(TimerTick, 0)
        return
    }
    if (A_TickCount < nextAt)
        return

    if (queue.Length = 0) {
        running := false
        SetTimer(TimerTick, 0)
        return
    }

    step := queue.RemoveAt(1)
    switch step.type {
        case "send":
            Send(step.data)
            ; Continue immediately; sleep-steps enforce waits
        case "sleep":
            nextAt := A_TickCount + step.data
            return
        case "click":
            ; Click at current mouse position without moving it
            btn := step.HasProp("btn") ? step.btn : "L"
            cnt := step.HasProp("cnt") ? step.cnt : 1
            if (btn = "R") {
                ; Click right button at current position, 'cnt' times
                Click ,, "Right", cnt
            } else {
                ; Click left button at current position, 'cnt' times
                Click ,, "Left", cnt
            }
            ; no implicit delay here; rely on following sleep-step
        default:
            ; unknown step -> ignore
    }
    ; allow multiple non-sleep steps in one tick
}

StartRun() {
    global running, nextAt
    if running
        return
    running := true
    nextAt := 0
    SetTimer(TimerTick, 5) ; tick every 5 ms
}

StopRun() {
    global running, queue
    running := false
    queue := []
    SetTimer(TimerTick, 0)
    ; try to bail out of menus/popups
    Send("{Esc}{Esc}")
}

; ============ HOTKEYS ============

; Start: Ctrl+Shift+.
^+.:: {
    ResolveTimings()
    BuildRun(repeats)
    StartRun()
}

; STOP: Alt+,
!,:: {
    StopRun()
}

; Toggle turbo timings
^+t:: {
    global TurboMode
    TurboMode := !TurboMode
    ResolveTimings()
    TrayTip("Teams Reactions", "Turbo: " (TurboMode ? "ON" : "OFF"), 900)
}
```

It was funny for a day, but people got annoyed on the second day and stopped writing to me for fear that I would spam them xD.

Therefore, the two key functions of the script are:

1. Calling employees to the computer because something is beeping non-stop.

2. Making your workload lighter because people don’t want to write to you for fear of your reactions.

![Dr. Evil](drevil.webp)

A mass-reaction “spammer” in Teams or chat could be abused as a distraction technique during an attack — flooding users with notification sounds or drawing their attention to the chat while the attacker carries out other malicious actions elsewhere. This makes it a potential element of a social-engineering or diversion attack, even if it looks like a prank on the surface.

Personnel focus on the “funny incident” while the actual attack is taking place elsewhere.

Could it be? Similar things have already been done: [Zoombombing](https://en.wikipedia.org/wiki/Zoombombing).
