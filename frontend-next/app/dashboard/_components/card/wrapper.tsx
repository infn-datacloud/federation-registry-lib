import { Card, CardActionArea, CardHeader, CardMedia } from "@mui/material";
import Link from "next/link";
import React from "react";
import { cardMaxWidth, cardMediaHeight } from "../../_lib/constants";

const cardMediaImage =
  "https://www.datanami.com/wp-content/uploads/2019/06/cloud_digital_shutterstock_Phonlamai-Photo-300x200.jpg";

export default function CardWrapper({
  kind,
  name,
  uid,
  children,
}: {
  kind: string;
  uid: string;
  name: string;
  children?: React.ReactNode;
}) {
  return (
    <Link href={`/dashboard/${kind}/${uid}`}>
      <Card sx={{ maxWidth: cardMaxWidth }}>
        <CardActionArea>
          <CardHeader title={name} />
          <CardMedia
            component="img"
            height={cardMediaHeight}
            image={cardMediaImage}
            alt="Cloud provider image"
          />
          {children}
        </CardActionArea>
      </Card>
    </Link>
  );
}
