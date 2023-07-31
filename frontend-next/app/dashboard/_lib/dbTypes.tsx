import { Url } from "next/dist/shared/lib/router/router";

export type AuthDetails = {
  idp_name: string;
  protocol: string;
};

export type Flavor = {
  uid: string;
  name: string;
  uuid: string;
  num_vcpus: number;
  num_gpus: number;
  ram: number;
  disk: number;
  infiniband_support: boolean;
  gpu_model?: string;
  gpu_vendor?: string;
};

export type IdentityProvider = {
  uid: string;
  endpoint: Url;
  group_claim: string;
  relationship?: AuthDetails;
};

export type Image = {
  uid: string;
  name: string;
  uuid: string;
  os: string;
  distribution: string;
  version: string;
  architecture: string;
  cuda_support: boolean;
  gpu_driver: boolean;
  creation_time?: Date;
};

export type Location = {
  uid: string;
  name: string;
  country: string;
  latitude?: number;
  longitude?: number;
  providers?: Provider[];
};

export type Project = {
  uid: string;
  name: string;
  uuid: string;
  public_network_name?: string;
  private_network_name?: string;
  private_network_proxy_host?: string;
  private_network_proxy_user?: string;
};

export type Provider = {
  uid: string;
  name: string;
  is_public: boolean;
  support_emails: string[];
  location?: Location;
  flavors?: Flavor[];
  identity_providers?: IdentityProvider[];
  images?: Image[];
  projects?: Project[];
  services?: Service[];
};

export type Service = {
  uid: string;
  endpoint: Url;
  type: string;
};

export type SLA = {
  uid: string;
  start_date: Date;
  end_date?: Date;
  document_uuid: string;
  user_group?: UserGroup;
  project?: Project;
};

export type UserGroup = {
  uid: string;
  name: string;
};
