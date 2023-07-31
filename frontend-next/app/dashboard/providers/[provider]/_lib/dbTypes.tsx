import {
  AuthDetailsBase,
  FlavorBase,
  IdentityProviderBase,
  ImageBase,
  LocationBase,
  ProjectBase,
  ProviderBase,
  ServiceBase,
} from "../../../_lib/dbTypes";

export interface IdentityProvider extends IdentityProviderBase {
  relationship: AuthDetailsBase;
}

export interface Provider extends ProviderBase {
  location?: LocationBase;
  flavors: FlavorBase[];
  identity_providers: IdentityProvider[];
  images: ImageBase[];
  projects: ProjectBase[];
  services: ServiceBase[];
}
