"use client";

import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
} from "@mui/material";
import { ChangeEvent, useState } from "react";
import { IdentityProvider } from "../_lib/dbTypes";

export default function IdentityProvidersTable({
  items,
}: {
  items: IdentityProvider[];
}) {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event: ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(+event.target.value);
    setPage(0);
  };

  const rowsPerPageOptions = [5, 10, 25];

  return (
    <Paper>
      <TableContainer>
        <Table sx={{ minWidth: 650 }}>
          <TableHead>
            <TableRow>
              <TableCell>Endpoint</TableCell>
              <TableCell>Group Claim</TableCell>
              <TableCell>Communication Name</TableCell>
              <TableCell>Communication Protocol</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {items
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((item, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row">
                    {item.endpoint.toString()}
                  </TableCell>
                  <TableCell>{item.group_claim}</TableCell>
                  <TableCell>{item.relationship?.idp_name}</TableCell>
                  <TableCell>{item.relationship?.protocol}</TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={rowsPerPageOptions}
        component="div"
        count={items.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
}
