import { LocationBase, ProviderBase } from "@/app/dashboard/_lib/dbTypes";

export interface Location extends LocationBase {
  providers: ProviderBase[];
}
