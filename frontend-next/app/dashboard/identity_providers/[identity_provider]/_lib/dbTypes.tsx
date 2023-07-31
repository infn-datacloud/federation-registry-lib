import {
  AuthDetailsBase,
  IdentityProviderBase,
  ProviderBase,
  UserGroupBase,
} from "@/app/dashboard/_lib/dbTypes";

export interface Provider extends ProviderBase {
  relationship: AuthDetailsBase;
}

export interface IdentityProvider extends IdentityProviderBase {
  providers: Provider[];
  user_groups: UserGroupBase[];
}
