class Project {
    constructor({pid, name, create_time}) {
        this.pid = pid;
        this.name = name;
        this.create_time = create_time;
        this.current_fetch_time = 0;
    }
}


class Segment {
    constructor({sid, time, waves}) {
        this.sid = sid;
        this.time = time;
        this.waves = waves;
    }
}


class Wave {
    constructor({value, label}) {
        this.value = value;
        this.label = label;
    }
}
