
import { defineStore } from 'pinia'
import { $apifetch } from '~/composable/fetch'

export interface UserData {
    limit: number;
    used: number;
    next_reset: Date;
}

const USER_DATA = 'userdata';
export const useUserStore = defineStore('userStore', () => {
    const userdata: Ref<UserData | null > = ref(null);
    load();
    function updateUser() {
        $apifetch('/api/user/', {
            method: 'GET',
        }).then((data) => {
            userdata.value = { limit: data.limit, used: data.usage, next_reset: new Date(data.next_reset) };
            save();
        })
    }

    function save() {
        sessionStorage.setItem(USER_DATA, JSON.stringify(userdata.value));
    }

    function load() {
        const data = sessionStorage.getItem(USER_DATA);
        if (data) {
            let userdataResponse: UserData = JSON.parse(data);
            // TODO: handle timezones
            userdataResponse.next_reset = new Date(userdataResponse.next_reset);

            if (userdataResponse.next_reset.getTime() > (new Date()).getTime()) {
                userdata.value = userdataResponse;
                return;
            }
        }
        updateUser();
    }
    return { userdata, updateUser, load}
})
