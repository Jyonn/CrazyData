class Pager {
    constructor({count, api, last=0}) {
        this.count = count;
        this.last = last;
        this.api = api;
        this.fetching = false;
    }

    next() {
        return new Promise((resolve, reject) => {
            if (this.last === null || this.fetching) {
                resolve(null);
            }
            this.fetching = true;
            Request.get(this.api, {count: this.count, last: this.last})
                .then(resp => {
                    this.last = resp.next_value;
                    this.fetching = false;
                    resolve(resp);
                })
                .catch((error) => {
                    this.fetching = false;
                    reject(error);
                })
        });
    }
}
