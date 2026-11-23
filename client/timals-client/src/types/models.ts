export interface User {
    id: number;
    username: string;
    email: string;
    //hashed_password: string;
    first_name: string | null;
    last_name: string | null;
    is_admin: boolean;
}

export interface Category {
    id: number;
    name: string;
    user_id: number;
}

export interface TimerPreset {
    id: number;
    name: string;
    worktime: number;
    breaktime: number;
    resttime: number;
    cycle: number;
    user_id: number;
}

export interface Activity {
    id: number;
    name: string;
    user_id: number;
    category_id: number | null;
}

export interface ActivityLog {
    id: number;
    user_id: number;
    activity_id: number;
    finished: boolean;
    date: string;
}

export interface CalendarEvent {
    id: number;
    name: string | null;
    user_id: number;
    category_id: number | null;
    start_time: string;
    end_time: string;
    whole_day: boolean;
    repeat: string | null;
    note: string | null;
    place: string | null;
    calendarreminders: CalendarReminder[] | null;
}

export interface CalendarEventSimple {
    id: number;
    name: string | null;
    user_id: number;
    category_id: number | null;
    start_time: string;
    end_time: string;
}

export interface CalendarReminder {
    id: number;
    event_id: number;
    minutes_before: number | null;
}