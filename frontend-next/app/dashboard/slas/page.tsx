"use client";

import { Grid } from "@mui/material";
import SLACardContent from "./_components/slaCardContent";
import Loading from "../slas/loading";
import { useSLAs } from "../_lib/crud";
import CardWrapper from "../_components/card/wrapper";
import { SLA } from "./_lib/dbTypes";

export default function Page() {
  const { slas } = useSLAs();
  const children = slas ? (
    slas.map((sla: SLA, index: number) => (
      <Grid item key={index}>
        <CardWrapper kind="slas" name="SLA" uid={sla.uid}>
          <SLACardContent item={sla} />
        </CardWrapper>
      </Grid>
    ))
  ) : (
    <Loading />
  );
  return (
    <Grid container spacing={2}>
      {children}
    </Grid>
  );
}
