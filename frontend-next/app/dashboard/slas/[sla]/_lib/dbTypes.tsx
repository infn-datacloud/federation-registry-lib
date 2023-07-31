import {
  IdentityProviderBase,
  ProjectBase,
  ProviderBase,
  SLABase,
  UserGroupBase,
} from "@/app/dashboard/_lib/dbTypes";

export interface Project extends ProjectBase {
  provider: ProviderBase;
}

export interface UserGroup extends UserGroupBase {
  identity_provider: IdentityProviderBase;
}

export interface SLA extends SLABase {
  user_group: UserGroup;
  project: Project;
}
