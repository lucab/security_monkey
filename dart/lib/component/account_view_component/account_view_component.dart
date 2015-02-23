part of security_monkey;

@Component(
    selector: 'accountview',
    templateUrl: 'packages/security_monkey/component/account_view_component/account_view_component.html',
    //cssUrl: const ['/css/bootstrap.min.css'],
    useShadowDom: false
)
class AccountViewComponent implements ScopeAware {

    RouteProvider routeProvider;
    Router router;
    List<User> users = new List<User>();
    List<String> owners = new List<String>();
    Account account;
    bool create = false;
    bool _as_loaded = false;
    bool _is_error = false;
    String err_message = "";
    ObjectStore store;

    AccountViewComponent(this.routeProvider, this.router, this.store) {
        //TODO: directly use 'account.owners' and ng-options
        //      instead of 'owners' (List<int> vs List<String>)
        this.store = store;
        store.customQueryList(User, new CustomRequestParams(method: "GET", url: "$API_HOST/users", withCredentials: true)).then((List<User> userlist) {
            this.users = userlist;
        });
        // If the URL has an ID, then let's view/edit
        if (routeProvider.parameters.containsKey("accountid")) {
            store.one(Account, routeProvider.parameters['accountid']).then((Account account) {
                this.account = account;
                _as_loaded = true;
                for (int o in account.owners) {
                    this.owners.add(o.toString());
                }
            });
            create = false;
        } else {
            // If the URL does not have an ID, then let's create
            account = new Account();
            create = true;
        }
    }

    void set scope(Scope scope) {
        scope.on("globalAlert").listen(this._showMessage);
    }

    get isLoaded => create || _as_loaded;
    get isError => _is_error;

    void _showMessage(ScopeEvent event) {
        this._is_error = true;
        this.err_message = event.data;
    }

    void saveAccount() {
        this.account.owners.clear();
        this.owners.forEach((o) => this.account.owners.add(int.parse(o)));
        if (create) {
            this.store.create(this.account).then((CommandResponse r) {
                int id = r.content['id'];
                router.go('viewaccount', {
                    'accountid': id
                });
            });
        } else {
            this.store.update(this.account);
        }
        print("o: ${this.owners}");
        print("ao: ${this.account.owners}");
    }

    /// Users can just make an account inactive.
    /// Not sure if we should expose delete.
    void deleteAccount() {
        this.store.delete(this.account).then((_) {
            router.go('settings', {});
        });
    }

    bool isUserOwner(User user) {
        return this.account.owners.any((int id) => (id == user.id));
    }

}
