"use client";

import { Image } from "@/app/dashboard/_lib/dbTypes";
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

export default function ImagesTable({ items }: { items: Image[] }) {
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
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>UUID</TableCell>
              <TableCell>OS</TableCell>
              <TableCell>Distribution</TableCell>
              <TableCell>Version</TableCell>
              <TableCell>Architecture</TableCell>
              <TableCell>CUDA Support</TableCell>
              <TableCell>GPU Driver Support</TableCell>
              <TableCell>Creation time</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {items
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((item, index) => (
                <TableRow key={index}>
                  <TableCell component="th" scope="row">
                    {item.name}
                  </TableCell>
                  <TableCell>{item.uuid}</TableCell>
                  <TableCell>{item.os}</TableCell>
                  <TableCell>{item.distribution}</TableCell>
                  <TableCell>{item.version}</TableCell>
                  <TableCell>{item.architecture}</TableCell>
                  <TableCell>
                    {item.cuda_support ? "Enabled" : "Disabled"}
                  </TableCell>
                  <TableCell>
                    {item.gpu_driver ? "Enabled" : "Disabled"}
                  </TableCell>
                  <TableCell>{item.creation_time?.toISOString()}</TableCell>
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
