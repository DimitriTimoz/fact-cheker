
import { defineStore } from 'pinia'
import { $apifetch } from '~/composable/fetch'

export interface RateLimit {
    limit: number;
    used: number;
    next_reset: Date;
}

export const useUserStore = defineStore('userStore', () => {
    const ratelimit: Ref<RateLimit | null > = ref(null);
    load();
    function updateRate() {
        $apifetch('/api/rate-limit/', {
            method: 'GET',
        }).then((data) => {
            ratelimit.value = { limit: data.limit, used: data.usage, next_reset: new Date(data.next_reset) };
            save();
        })
    }

    function save() {
        sessionStorage.setItem('ratelimit', JSON.stringify(ratelimit.value));
    }

    function load() {
        const data = sessionStorage.getItem('ratelimit');
        if (data) {
            let ratelimitResponse: RateLimit = JSON.parse(data);
            // TODO: handle timezones
            ratelimitResponse.next_reset = new Date(ratelimitResponse.next_reset);

            if (ratelimitResponse.next_reset.getTime() > (new Date()).getTime()) {
                ratelimit.value = ratelimitResponse;
                return;
            }
        }
        updateRate();
    }
    return { ratelimit, updateRate }
})
