import { Url } from "next/dist/shared/lib/router/router";

export interface AuthDetailsBase {
  idp_name: string;
  protocol: string;
}

export interface FlavorBase {
  uid: string;
  name: string;
  uuid: string;
  vcpus: number;
  ram: number;
  disk: number;
  swap: number;
  infiniband_support: boolean;
  num_gpus: number;
  gpu_model?: string;
  gpu_vendor?: string;
}

export interface IdentityProviderBase {
  uid: string;
  endpoint: Url;
  group_claim: string;
}

export interface ImageBase {
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
}

export interface LocationBase {
  uid: string;
  name: string;
  country: string;
  latitude?: number;
  longitude?: number;
}

export interface ProjectBase {
  uid: string;
  name: string;
  uuid: string;
  public_network_name?: string;
  private_network_name?: string;
  private_network_proxy_host?: string;
  private_network_proxy_user?: string;
}

export interface ProviderBase {
  uid: string;
  name: string;
  is_public: boolean;
  support_emails: string[];
}

export interface ServiceBase {
  uid: string;
  endpoint: Url;
  type: string;
}

export interface SLABase {
  uid: string;
  start_date: Date;
  end_date?: Date;
  document_uuid: string;
}

export interface UserGroupBase {
  uid: string;
  name: string;
}
