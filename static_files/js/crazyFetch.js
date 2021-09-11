class CrazyFetch {
    constructor(project) {
        this.project = project;
        this.pager = new Pager({count: 30, api: `https://data.6-79.cn/v1/segment?pid=${this.project.pid}`, last: 0});
        this.is_fetching = false;
    }

    async fetchNewData() {
        let dataFlow = [];

        if (this.is_fetching) {
            return dataFlow;
        }

        this.is_fetching = true;

        while (true) {
            this.pager.last = this.project.current_fetch_time;
            while (this.pager.last !== null) {
                let data;
                try {
                    data = await this.pager.next();
                } catch (error) {
                    console.warn('fetch failed, retrying...')
                    break;
                }
                if (data === null) {
                    break;
                }
                data = data.object_list;
                if (data.length) {
                    this.project.current_fetch_time = Math.max.apply(null, data.map(d => d.time));
                    dataFlow = dataFlow.concat(data);
                }
            }
            if (dataFlow.length) {
                break;
            }
            await new Promise(resolve => {
                setTimeout(() => resolve(), 5000);
            });
        }

        this.is_fetching = false;

        return dataFlow;
    }
}
